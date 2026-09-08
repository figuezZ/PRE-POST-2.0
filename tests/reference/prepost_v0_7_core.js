
  "use strict";
  globalThis.PrePostCore = (() => {
    const INCH_M = 0.0254;
    const FOOT_M = 0.3048;
    const LBF_N = 0.45359237 * 9.80665;
    const KIP_N = 1000 * LBF_N;
    const PSI_PA = LBF_N / (INCH_M ** 2);

    const units = {
      SI: {
        span: ["m", 1, 3], sectionLength: ["m", 1, 4], unitWeight: ["kN/m³", 1e3, 3],
        stress: ["MPa", 1e6, 3], lineLoad: ["kN/m", 1e3, 3], force: ["kN", 1e3, 3],
        steelArea: ["mm²", 1e-6, 3], sectionArea: ["m²", 1, 6], inertia: ["m⁴", 1, 6],
        sectionModulus: ["m³", 1, 6], moment: ["kN·m", 1e3, 3]
      },
      USCS: {
        span: ["ft", FOOT_M, 3], sectionLength: ["in", INCH_M, 3], unitWeight: ["pcf", LBF_N / (FOOT_M ** 3), 3],
        stress: ["psi", PSI_PA, 2], lineLoad: ["kip/ft", KIP_N / FOOT_M, 4], force: ["kip", KIP_N, 3],
        steelArea: ["in²", INCH_M ** 2, 4], sectionArea: ["in²", INCH_M ** 2, 3], inertia: ["in⁴", INCH_M ** 4, 3],
        sectionModulus: ["in³", INCH_M ** 3, 3], moment: ["kip·ft", KIP_N * FOOT_M, 3]
      }
    };

    function unit(system, quantity) {
      if (!units[system] || !units[system][quantity]) throw new Error("Sistema o magnitud no reconocida.");
      const [symbol, factor, decimals] = units[system][quantity];
      return { symbol, factor, decimals };
    }
    function toSI(value, quantity, system) { return Number(value) * unit(system, quantity).factor; }
    function fromSI(value, quantity, system) { return Number(value) / unit(system, quantity).factor; }
    function positive(name, value) {
      if (!Number.isFinite(value) || value <= 0) throw new Error(`${name} debe ser mayor que cero.`);
    }
    function nonnegative(name, value) {
      if (!Number.isFinite(value) || value < 0) throw new Error(`${name} no puede ser negativo.`);
    }

    function sectionProperties(input) {
      return componentProperties(input.components || [{name:'Rectángulo',sign:1,b:input.width_m,h:input.height_m,y:0}], input.unit_weight_n_m3);
    }

    function uniformLoadEffects(w, span) {
      nonnegative("La carga uniforme", w);
      positive("La luz", span);
      const reaction = w * span / 2;
      if (!Number.isFinite(reaction) || !Number.isFinite(w*span**2/8)) throw new Error('Magnitudes fuera del rango numérico. Revise las unidades.');
      return { reaction_n: reaction, max_shear_n: reaction, midspan_moment_n_m: w * span ** 2 / 8 };
    }

    function elasticStresses(section, force, eccentricity, externalMoment) {
      positive("La fuerza de pretensado", force);
      const prestressMoment = force * eccentricity;
      const resultantMoment = prestressMoment + externalMoment;
      const axial = -force / section.area_m2;
      const topY = section.height_m - section.centroid_from_bottom_m;
      return {
        top_pa: axial - resultantMoment * topY / section.inertia_m4,
        bottom_pa: axial + resultantMoment * section.centroid_from_bottom_m / section.inertia_m4,
        axial_component_pa: axial,
        prestress_moment_n_m: prestressMoment,
        external_moment_n_m: externalMoment,
        resultant_moment_n_m: resultantMoment
      };
    }

    function validate(input) {
      positive("La luz", input.span_m); positive("El ancho", input.width_m); positive("El alto", input.height_m);
      positive("El peso específico", input.unit_weight_n_m3); positive("f'ci", input.fci_pa); positive("f'c", input.fc_pa);
      if (input.fc_pa < input.fci_pa) throw new Error("f'c no puede ser menor que f'ci.");
      nonnegative("La carga muerta adicional", input.dead_load_n_m); nonnegative("La carga viva", input.live_load_n_m);
      positive("La fuerza inicial", input.initial_force_n); positive("El área de acero", input.steel_area_m2);
      if (!Number.isFinite(input.loss_ratio) || input.loss_ratio < 0 || input.loss_ratio >= 1) throw new Error("La pérdida debe estar entre 0 % y menos de 100 %.");
      if (!Number.isFinite(input.eccentricity_m)) throw new Error('La excentricidad debe ser finita.');
      if (input.initial_force_n / input.steel_area_m2 > 1860e6) throw new Error("La tensión inicial del acero supera 1860 MPa.");
    }

    function analyze(input) {
      validate(input);
      const section = sectionProperties(input);
      const tendonY = section.centroid_from_bottom_m + input.eccentricity_m;
      if (!containsConcrete(section.components, 0, tendonY)) throw new Error('El centro del tendón debe permanecer dentro de la sección de hormigón, fuera de vacíos.');
      const transferLoad = section.self_weight_n_m;
      const transferEffects = uniformLoadEffects(transferLoad, input.span_m);
      const transferStress = elasticStresses(section, input.initial_force_n, input.eccentricity_m, transferEffects.midspan_moment_n_m);
      const effectiveForce = input.initial_force_n * (1 - input.loss_ratio);
      const serviceLoad = transferLoad + input.dead_load_n_m + input.live_load_n_m;
      const serviceEffects = uniformLoadEffects(serviceLoad, input.span_m);
      const serviceStress = elasticStresses(section, effectiveForce, input.eccentricity_m, serviceEffects.midspan_moment_n_m);
      return {
        input, section,
        transfer: {
          uniform_load_n_m: transferLoad, reaction_n: transferEffects.reaction_n,
          max_shear_n: transferEffects.max_shear_n, midspan_moment_n_m: transferEffects.midspan_moment_n_m,
          initial_steel_stress_pa: input.initial_force_n / input.steel_area_m2, stress: transferStress
        },
        service: {
          effective_force_n: effectiveForce, effective_steel_stress_pa: effectiveForce / input.steel_area_m2,
          uniform_load_n_m: serviceLoad, reaction_n: serviceEffects.reaction_n,
          max_shear_n: serviceEffects.max_shear_n, midspan_moment_n_m: serviceEffects.midspan_moment_n_m,
          stress: serviceStress
        }
      };
    }

    function beamDiagram(w, span, count = 101) {
      uniformLoadEffects(w,span);
      if (!Number.isInteger(count) || count<2 || count>10001) throw new Error('Cantidad de puntos inválida.');
      const reaction = w * span / 2;
      return Array.from({length: count}, (_, index) => {
        const x = span * index / (count - 1);
        return { x, shear: reaction - w * x, moment: reaction * x - w * x ** 2 / 2 };
      });
    }

    function stressProfile(height, top, bottom, count = 51, centroid = height / 2) {
      positive('Altura',height);
      if (![top,bottom,centroid].every(Number.isFinite) || !Number.isInteger(count) || count<2 || count>10001) throw new Error('Datos de perfil inválidos.');
      return Array.from({length: count}, (_, index) => {
        const ratio = index / (count - 1);
        return { x: -centroid + height * ratio, stress: bottom + (top - bottom) * ratio };
      });
    }

    // Rectángulos centrados en el eje vertical: teorema de ejes paralelos.
    // Referencias: docs/taller_visual.md y fórmulas del núcleo Python.
    function componentProperties(components, gamma) {
      if (!Array.isArray(components) || !components.length || components.length > 24) throw new Error('Use entre 1 y 24 componentes.');
      positive('El peso específico', gamma);
      const parts = components.map((p,index) => {
        positive('Ancho del componente '+(index+1),p.b); positive('Alto del componente '+(index+1),p.h);
        nonnegative('Cota inferior',p.y);
        if (![1,-1].includes(p.sign)) throw new Error('El signo del componente debe ser +1 o −1.');
        return {...p,name:String(p.name || 'Componente '+(index+1))};
      });
      const solids = parts.filter(p=>p.sign===1).sort((a,b)=>a.y-b.y), holes=parts.filter(p=>p.sign===-1);
      if (!solids.length || Math.abs(solids[0].y)>1e-10) throw new Error('El primer sólido debe comenzar en la base Y = 0.');
      for (let j=1;j<solids.length;j++) {
        if (Math.abs(solids[j].y-solids[j-1].y-solids[j-1].h)>1e-9) throw new Error('Los sólidos deben tocarse por sus caras horizontales, sin superposición ni separación.');
      }
      holes.forEach((p,j)=>{
        if (!solids.some(s=>p.b<s.b && p.y>=s.y-1e-10 && p.y+p.h<=s.y+s.h+1e-10)) throw new Error('Cada vacío debe quedar en un solo sólido y ser más estrecho que él.');
        if (holes.slice(0,j).some(q=>Math.min(p.y+p.h,q.y+q.h)-Math.max(p.y,q.y)>1e-10)) throw new Error('Los vacíos no pueden superponerse.');
      });
      const height = Math.max(...solids.map(p=>p.y+p.h)), width=Math.max(...solids.map(p=>p.b));
      let covered=0;
      holes.slice().sort((a,b)=>a.y-b.y).forEach(p=>{if(p.y<=covered+1e-10)covered=Math.max(covered,p.y+p.h);});
      if(covered>=height-1e-10) throw new Error('Los vacíos separan completamente la sección en dos piezas.');
      const grossArea=solids.reduce((a,p)=>a+p.b*p.h,0);
      const area=parts.reduce((a,p)=>a+p.sign*p.b*p.h,0);
      positive('Área neta',area);
      const centroid=parts.reduce((a,p)=>a+p.sign*p.b*p.h*(p.y+p.h/2),0)/area;
      const rows=parts.map(p=>({...p,area:p.sign*p.b*p.h,centroid:p.y+p.h/2,d:p.y+p.h/2-centroid,
        own:p.sign*p.b*p.h**3/12,parallel:p.sign*p.b*p.h*(p.y+p.h/2-centroid)**2}));
      const inertia=rows.reduce((a,p)=>a+p.own+p.parallel,0);
      positive('Inercia',inertia);
      const grossCentroid=solids.reduce((a,p)=>a+p.b*p.h*(p.y+p.h/2),0)/grossArea;
      const grossInertia=solids.reduce((a,p)=>a+p.b*p.h**3/12+p.b*p.h*(p.y+p.h/2-grossCentroid)**2,0);
      return {components:parts,rows,area_m2:area,gross_area_m2:grossArea,gross_inertia_m4:grossInertia,
        gross_centroid_m:grossCentroid,centroid_from_bottom_m:centroid,inertia_m4:inertia,
        section_modulus_top_m3:inertia/(height-centroid),section_modulus_bottom_m3:inertia/centroid,
        self_weight_n_m:area*gamma,height_m:height,width_m:width};
    }
    function containsConcrete(parts,x,y) {
      const height=Math.max(...parts.filter(p=>p.sign===1).map(p=>p.y+p.h));
      return y>0 && y<height && parts.some(p=>p.sign===1 && Math.abs(x)<p.b/2 && y>=p.y && y<=p.y+p.h) &&
        !parts.some(p=>p.sign===-1 && Math.abs(x)<=p.b/2 && y>=p.y && y<=p.y+p.h);
    }
    function stageAt(result,stage,x) {
      if (!['transfer','service'].includes(stage)) throw new Error('Etapa inválida.');
      if (!Number.isFinite(x) || x<0 || x>result.input.span_m) throw new Error('Posición fuera de la luz.');
      const force=stage==='transfer'?result.input.initial_force_n:result.service.effective_force_n;
      const w=result[stage].uniform_load_n_m,L=result.input.span_m;
      const reaction=w*L/2, moment=reaction*x-w*x*x/2;
      const stress=elasticStresses(result.section,force,result.input.eccentricity_m,moment);
      const slope=-stress.resultant_moment_n_m/result.section.inertia_m4;
      const zero=Math.abs(slope)<1e-12?null:-stress.axial_component_pa/slope;
      return {x,force,w,reaction,shear:reaction-w*x,moment,stress,slope,zero,
        zeroInside:zero!==null && zero>=-result.section.centroid_from_bottom_m && zero<=result.section.height_m-result.section.centroid_from_bottom_m};
    }
    function fiberAt(result,stage,x,y) {
      if(!Number.isFinite(y) || y < -result.section.centroid_from_bottom_m-1e-10 || y > result.section.height_m-result.section.centroid_from_bottom_m+1e-10) throw new Error('Fibra fuera de la altura de la sección.');
      const s=stageAt(result,stage,x);
      return {stress:s.stress.axial_component_pa+s.slope*y,axial:s.stress.axial_component_pa,
        prestress:-s.stress.prestress_moment_n_m*y/result.section.inertia_m4,
        external:-s.moment*y/result.section.inertia_m4,
        concrete:containsConcrete(result.section.components,0,y+result.section.centroid_from_bottom_m)};
    }
    function memory(result,stage,x) {
      const p=result.section,i=result.input,s=stageAt(result,stage,x), cy=p.centroid_from_bottom_m;
      const n=v=>Number(v).toExponential(7);
      const steps=[
        ['Área de hormigón','A = Σ sᵢ bᵢ hᵢ',p.rows.map(r=>n(r.area)).join(' + '),p.area_m2,'m²'],
        ['Centroide','Ȳ = Σ(Aᵢ Yᵢ)/A',p.rows.map(r=>'('+n(r.area)+' × '+n(r.centroid)+')').join(' + ')+'; dividir por '+n(p.area_m2),cy,'m'],
        ['Inercia centroidal','I = Σ (sᵢ bᵢ hᵢ³/12 + Aᵢ dᵢ²)',p.rows.map(r=>'('+n(r.own)+' + '+n(r.parallel)+')').join(' + '),p.inertia_m4,'m⁴'],
        ['Distancia superior','cₛ = h − Ȳ',n(p.height_m)+' − '+n(cy),p.height_m-cy,'m'],
        ['Distancia inferior','cᵢ = Ȳ',n(cy),cy,'m'],
        ['Módulo superior','Wₛ = I/cₛ',n(p.inertia_m4)+' / '+n(p.height_m-cy),p.section_modulus_top_m3,'m³'],
        ['Módulo inferior','Wᵢ = I/cᵢ',n(p.inertia_m4)+' / '+n(cy),p.section_modulus_bottom_m3,'m³'],
        ['Peso propio','wpp = γ A',n(i.unit_weight_n_m3)+' × '+n(p.area_m2),p.self_weight_n_m,'N/m'],
        ['Fuerza de etapa',stage==='service'?'Pe = (1 − pérdida) Pi':'P = Pi',stage==='service'?'(1 − '+n(i.loss_ratio)+') × '+n(i.initial_force_n):n(i.initial_force_n),s.force,'N'],
        ['Tensión del acero','fp = P/Ap',n(s.force)+' / '+n(i.steel_area_m2),s.force/i.steel_area_m2,'Pa'],
        ['Carga de etapa',stage==='service'?'w = wpp + g + q':'w = wpp',stage==='service'?[p.self_weight_n_m,i.dead_load_n_m,i.live_load_n_m].map(n).join(' + '):n(p.self_weight_n_m),s.w,'N/m'],
        ['Reacción','R = w L/2',n(s.w)+' × '+n(i.span_m)+' / 2',s.reaction,'N'],
        ['Corte en x','V(x) = R − wx',n(s.reaction)+' − '+n(s.w)+' × '+n(x),s.shear,'N'],
        ['Momento en x','M(x) = Rx − wx²/2',n(s.reaction)+' × '+n(x)+' − '+n(s.w)+' × '+n(x)+'²/2',s.moment,'N·m'],
        ['Momento del pretensado','Mp = P e',n(s.force)+' × '+n(i.eccentricity_m),s.stress.prestress_moment_n_m,'N·m'],
        ['Momento resultante','Mr = Mp + M(x)',n(s.stress.prestress_moment_n_m)+' + '+n(s.moment),s.stress.resultant_moment_n_m,'N·m'],
        ['Compresión uniforme','σN = −P/A','−'+n(s.force)+' / '+n(p.area_m2),s.stress.axial_component_pa,'Pa']
      ];
      [['superior',p.height_m-cy],['inferior',-cy]].forEach(([name,y])=>{
        const f=fiberAt(result,stage,x,y);
        steps.push(['Tensión '+name,'σ(y) = −P/A − (P·e + M)·y/I','y = '+n(y)+' m; −'+n(s.force)+'/'+n(p.area_m2)+' − ('+n(s.force)+' × '+n(i.eccentricity_m)+' + '+n(s.moment)+') × '+n(y)+' / '+n(p.inertia_m4)+' = '+n(f.axial)+' + '+n(f.prestress)+' + '+n(f.external),f.stress,'Pa']);
      });
      return steps.map(([label,formula,substitution,value,unit])=>({label,formula,substitution,value,unit,
        reference:'Geometría: áreas compuestas y ejes paralelos. Estática: equilibrio. Tensiones: Clase 3 USS (2026), convención e hacia arriba.'}));
    }
    return { units, unit, toSI, fromSI, analyze, beamDiagram, stressProfile, componentProperties, containsConcrete, stageAt, fiberAt, memory };
  })();
