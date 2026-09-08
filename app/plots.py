"""Plotly representa los resultados de src/ y convierte unidades visibles."""
import plotly.graph_objects as go
from src.units import Quantity as Q, display_unit, from_si
from src.analysis.pipeline import diagrams, stress_profile, stress_field, stress_scale, stage_at

COLORS = {'transfer': '#2563eb', 'service': '#d97706'}
LABELS = {'transfer': 'Transferencia', 'service': 'Servicio'}


def beam_plots(result, system):
    figures = []
    for value, title, quantity in [('shear','Corte V(x)',Q.FORCE), ('moment','Momento M(x)',Q.MOMENT)]:
        fig = go.Figure()
        for stage in LABELS:
            points = diagrams(result, stage)
            fig.add_trace(go.Scatter(x=[from_si(p['x'], Q.SPAN, system) for p in points],
                y=[from_si(p[value], quantity, system) for p in points],
                name=LABELS[stage], line={'color':COLORS[stage]}))
        fig.update_layout(title=title, xaxis_title=f"x [{display_unit(system,Q.SPAN).symbol}]",
            yaxis_title=display_unit(system,quantity).symbol, template='plotly_white', height=350)
        figures.append(fig)
    return figures


def profile_plot(result, system, x):
    fig = go.Figure()
    for stage in LABELS:
        points = stress_profile(result, stage, x)
        fig.add_trace(go.Scatter(x=[from_si(p['stress'],Q.STRESS,system) for p in points],
            y=[from_si(p['y'],Q.SECTION_LENGTH,system) for p in points], name=LABELS[stage],line={'color':COLORS[stage]}))
    fig.add_vline(x=0, line_dash='dot', line_color='#64748b')
    fig.add_hline(y=0, line_dash='dot', line_color='#64748b')
    fig.update_layout(title=f'Perfil en x={from_si(x,Q.SPAN,system):.4g} {display_unit(system,Q.SPAN).symbol}',
        xaxis_title=f"Tensión [{display_unit(system,Q.STRESS).symbol}]",
        yaxis_title=f"y desde centroide [{display_unit(system,Q.SECTION_LENGTH).symbol}]", template='plotly_white')
    return fig


def section_plot(section, eccentricity, system, result=None, stage='service', x=0, y=None):
    c = lambda v: from_si(v,Q.SECTION_LENGTH,system)
    fig = go.Figure()
    cy = section.centroid_from_bottom_m
    if result is not None:
        xs, ys, z = stress_field(result,stage,x)
        limit = from_si(stress_scale(result),Q.STRESS,system)
        fig.add_trace(go.Heatmap(x=[c(v) for v in xs],y=[c(v) for v in ys],
            z=[[from_si(v,Q.STRESS,system) if v is not None else None for v in row] for row in z],
            zmin=-limit,zmax=limit,zmid=0,colorscale=[[0,'#2563eb'],[.5,'#ffffff'],[1,'#dc2626']],
            colorbar={'title':display_unit(system,Q.STRESS).symbol}, hoverongaps=False,
            hovertemplate='Horizontal: %{x:.4g}<br>y: %{y:.4g}<br>Tensión: %{z:.5g}<extra></extra>'))
    for p in section.components:
        fig.add_shape(type='rect',x0=c(-p.b/2),x1=c(p.b/2),y0=c(p.y-cy),y1=c(p.y+p.h-cy),
            line={'color':'#334155','dash':'dash' if p.sign == -1 else 'solid'},
            fillcolor='white' if p.sign == -1 else ('rgba(0,0,0,0)' if result else '#dce8f6'))
    fig.add_trace(go.Scatter(x=[0],y=[c(eccentricity)],mode='markers',name='Tendón equivalente',
        marker={'size':12,'color':'#d97706'},hovertemplate='e: %{y:.5g}<extra>Tendón</extra>'))
    fig.add_hline(y=0,line_dash='dot',line_color='#475569',annotation_text='Centroide')
    if result is not None:
        pos = stage_at(result,stage,x)
        if pos.zero_inside:
            fig.add_hline(y=c(pos.zero),line_color='#15803d',annotation_text='Tensión = 0')
    if y is not None:
        fig.add_hline(y=c(y),line_color='#9333ea',line_dash='dash',annotation_text='Fibra elegida')
    symbol = display_unit(system,Q.SECTION_LENGTH).symbol
    fig.update_layout(title=f'Sección: b={c(section.width_m):.4g}, h={c(section.height_m):.4g} {symbol}',
        template='plotly_white',xaxis_title=f'Horizontal [{symbol}]',yaxis_title=f'y desde centroide [{symbol}]',
        yaxis={'scaleanchor':'x','scaleratio':1},height=460,margin={'l':35,'r':35,'t':55,'b':35})
    return fig
