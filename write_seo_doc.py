"""
Script para escribir textos SEO de Diagonal CQ en Google Docs.
Formato: Arial 11, NORMAL_TEXT, prefijos H1:/H2:/H3: en negrita, tabla real.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from tools.calendar_tools import get_google_credentials
from googleapiclient.discovery import build

DOC_ID = "1mbkD6hmmUm944_653ptryd9MGR4dgqZZWovMTC6wiRs"
TAB_ID = "t.s1bg2uhcf7fd"

# ---------------------------------------------------------------------------
# CONTENIDO — (texto, negrita)
# ---------------------------------------------------------------------------
BLOCKS_BEFORE_TABLE = [
    ("Meta title: Reconstrucción Mamaria en Córdoba | Diagonal CQ", False),
    ("Meta description: Reconstrucción mamaria tras mastectomía en Córdoba. Implantes y tejido propio. Dr. Joan Benítez, cirujano plástico. Consulta sin compromiso.", False),
    ("URL slug: /reconstruccion-mamaria/", False),
    ("", False),
    ("H1: Reconstrucción mamaria: en qué consiste, técnicas y resultados reales", True),
    ("", False),
    ("La reconstrucción mamaria es un procedimiento de cirugía plástica y reparadora cuyo objetivo es restaurar la forma, el volumen y la simetría del pecho después de una mastectomía total o parcial. Es el procedimiento más frecuente dentro de la cirugía oncoplástica de mama y forma parte integral del tratamiento del cáncer de mama.", False),
    ("", False),
    ("A diferencia de los procedimientos estéticos convencionales, la reconstrucción mamaria no responde a un deseo de mejora estética electiva, sino a la necesidad médica y emocional de recuperar la integridad corporal tras una intervención oncológica. Por ello, su planificación, técnica y seguimiento están estrechamente vinculados al tratamiento oncológico global de la paciente.", False),
    ("", False),
    ("En España, la Ley 10/2010 de 9 de julio reconoce expresamente el derecho de toda paciente mastectomizada a recibir cirugía de reconstrucción mamaria, tanto en la sanidad pública como en el ámbito privado con cobertura de seguro médico. Este marco legal refuerza la importancia de que la paciente conozca sus opciones desde el momento del diagnóstico.", False),
    ("", False),
    ("En Diagonal CQ, en Córdoba, el Dr. Joan Benítez trabaja en coordinación con los equipos de oncología para ofrecer una valoración individualizada, honesta y centrada en las necesidades reales de cada paciente. En esta página explicamos en qué consiste la reconstrucción mamaria, qué técnicas existen, para qué pacientes está indicada cada una y qué resultados son realistas, desde un enfoque médico riguroso.", False),
    ("", False),
    ("[añadir imagen de contexto médico en consulta: médico explicando opciones de reconstrucción a una paciente, sin rostro identificable / consulta real de Diagonal CQ]", False),
    ("", False),
    # --- H2: Qué es
    ("H2: ¿Qué es la reconstrucción mamaria y cuándo está indicada?", True),
    ("Procedimiento quirúrgico que restaura la forma del pecho tras una mastectomía, integrado dentro del plan oncológico global de la paciente.", False),
    ("", False),
    ("La reconstrucción mamaria engloba un conjunto de técnicas quirúrgicas orientadas a recrear la forma, el volumen y, cuando es posible, la sensibilidad del pecho extirpado. Puede realizarse en el mismo acto quirúrgico que la mastectomía o en un momento posterior, dependiendo del protocolo oncológico, el estado de salud de la paciente y sus preferencias personales.", False),
    ("", False),
    ("La indicación más frecuente es la mastectomía por cáncer de mama, aunque también puede plantearse en casos de malformaciones congénitas de la mama, pérdida de tejido mamario por traumatismo grave o resultados insatisfactorios de cirugías previas.", False),
    ("", False),
    ("H3: ¿Qué se puede reconstruir exactamente?", True),
    ("La reconstrucción puede abarcar distintos componentes según las necesidades de cada paciente:", False),
    ("", False),
    ("— El volumen y la forma general del pecho.", False),
    ("— El contorno y la proyección de la mama.", False),
    ("— El complejo areola-pezón, habitualmente en una segunda fase quirúrgica o mediante tatuaje médico.", False),
    ("— La simetría con respecto al pecho contralateral, que en algunos casos puede requerir también cirugía sobre la mama sana (reducción, aumento o mastopexia).", False),
    ("", False),
    ("H3: Un derecho reconocido por ley en España", True),
    ("La Ley Orgánica 10/2010 de 9 de julio garantiza que toda mujer mastectomizada en España tiene derecho a acceder a cirugía de reconstrucción mamaria en condiciones de igualdad, independientemente de la comunidad autónoma en la que resida. En el ámbito privado, la mayoría de los seguros médicos con cobertura quirúrgica incluyen esta prestación.", False),
    ("", False),
    ("H3: Reconstrucción mamaria inmediata vs. reconstrucción diferida", True),
    ("La elección entre reconstrucción inmediata y diferida es una de las primeras decisiones clínicas que deben tomarse en coordinación con el equipo de oncología:", False),
    ("", False),
    ("Reconstrucción inmediata: se realiza en el mismo acto quirúrgico que la mastectomía. Reduce el impacto psicológico al no despertar sin el pecho, minimiza el número de intervenciones y, en casos seleccionados, permite conservar mayor cantidad de piel. No siempre es posible si la paciente va a recibir radioterapia postoperatoria, ya que esta puede comprometer el resultado.", False),
    ("", False),
    ("Reconstrucción diferida: se realiza semanas, meses o incluso años después de la mastectomía, una vez que el tratamiento oncológico ha finalizado. Permite planificar la técnica sin condicionantes urgentes y es la opción habitual cuando se prevé radioterapia postoperatoria.", False),
    ("", False),
    # --- H2: Técnicas
    ("H2: Técnicas de reconstrucción mamaria: ¿cuál es la adecuada para ti?", True),
    ("Existen dos grandes enfoques técnicos —con implantes y con tejido propio— cuya elección depende del diagnóstico individual, los tratamientos recibidos y las características físicas de la paciente.", False),
    ("", False),
    ("H3: Reconstrucción mamaria con implante directo", True),
    ("Consiste en colocar directamente un implante de silicona tras la mastectomía, aprovechando la cobertura cutánea y muscular disponible. Es la técnica más sencilla y de recuperación más rápida, pero requiere que exista suficiente tejido para cubrir y sostener el implante con seguridad. No está indicada cuando se prevé radioterapia postoperatoria, ya que esta aumenta considerablemente el riesgo de contractura capsular y complicaciones.", False),
    ("", False),
    ("H3: Reconstrucción con expansor tisular e implante en dos tiempos", True),
    ("En este enfoque, se coloca primero un expansor tisular (una prótesis hinchable que se rellena progresivamente con suero fisiológico en consulta) para estirar gradualmente la piel y crear el espacio necesario. En una segunda intervención, el expansor se sustituye por el implante definitivo de silicona. Es la opción más habitual cuando la cobertura cutánea inicial es insuficiente para una colocación directa. El proceso puede durar varios meses.", False),
    ("", False),
    ("H3: Reconstrucción mamaria con tejido propio: colgajos DIEP, TRAM y dorsal ancho", True),
    ("Utiliza tejido vivo de la propia paciente para reconstruir la mama, lo que ofrece un resultado más natural al tacto, mayor durabilidad a largo plazo y menor riesgo de rechazo. Los colgajos más utilizados son:", False),
    ("", False),
    ("— Colgajo DIEP (Deep Inferior Epigastric Perforator): utiliza piel y grasa del abdomen sin sacrificar el músculo recto abdominal. Es actualmente la técnica de referencia en reconstrucción con tejido propio por su excelente resultado y menor morbilidad en la zona donante.", False),
    ("— Colgajo TRAM (Transverse Rectus Abdominis Myocutaneous): también utiliza tejido abdominal, pero incluye parte del músculo recto. Ofrece buenos resultados pero con mayor impacto en la zona donante que el DIEP.", False),
    ("— Colgajo de dorsal ancho (Latissimus dorsi): utiliza piel y músculo de la espalda. Es técnicamente más sencillo que los colgajos abdominales y puede combinarse con un implante cuando el volumen del tejido donante es insuficiente.", False),
    ("", False),
    ("Todas estas técnicas dejan una cicatriz adicional en la zona donante, lo que debe valorarse junto con la paciente antes de la decisión.", False),
    ("", False),
    ("H3: Técnica combinada: tejido propio más implante", True),
    ("En determinados casos, cuando el volumen del tejido propio disponible es insuficiente para obtener el resultado deseado, se combina el colgajo con un implante. Esta combinación es especialmente útil en pacientes que han recibido radioterapia y en las que una reconstrucción solo con implante tendría un riesgo elevado de complicaciones.", False),
    ("", False),
    # --- H2: Indicaciones
    ("H2: ¿Para qué pacientes está indicada la reconstrucción mamaria?", True),
    ("Indicada en pacientes que han sido sometidas a mastectomía y desean restaurar la forma y simetría del pecho, siempre que su estado de salud lo permita.", False),
    ("", False),
    ("La reconstrucción mamaria puede plantearse en pacientes que:", False),
    ("", False),
    ("— Han sido sometidas a mastectomía unilateral o bilateral por cáncer de mama.", False),
    ("— Presentan malformaciones congénitas de la mama (aplasia, hipoplasia grave).", False),
    ("— Han sufrido pérdida de tejido mamario por traumatismo o quemadura.", False),
    ("— Buscan mejorar la simetría tras una mastectomía parcial o tumorectomía con resultado estético insatisfactorio.", False),
    ("— Son portadoras de mutaciones BRCA1 o BRCA2 y han optado por mastectomía profiláctica.", False),
    ("", False),
    ("No siempre es posible realizar la reconstrucción en el momento que la paciente desea. Algunos tratamientos oncológicos activos, especialmente la radioterapia en curso, pueden condicionar tanto el momento como la técnica más adecuada. La indicación definitiva se establece siempre en coordinación con el equipo oncológico.", False),
    ("", False),
    # --- H2: Beneficios
    ("H2: Beneficios realistas de la reconstrucción mamaria", True),
    ("Mejora documentada de la imagen corporal y el bienestar emocional, con resultados duraderos que deben valorarse con expectativas realistas.", False),
    ("", False),
    ("Los beneficios de la reconstrucción mamaria incluyen:", False),
    ("", False),
    ("— Restauración de la forma, el volumen y la simetría del pecho.", False),
    ("— Mejora significativa de la imagen corporal y la autoestima tras la mastectomía.", False),
    ("— Reducción del impacto psicológico asociado a la pérdida del pecho.", False),
    ("— Posibilidad de usar ropa normal y ropa interior sin prótesis externas.", False),
    ("— Resultado de larga duración, especialmente en técnicas con tejido propio.", False),
    ("— Opción de reconstrucción sin implantes para pacientes que prefieren tejido propio.", False),
    ("", False),
    ("Los resultados dependen de la técnica empleada, las características físicas individuales, los tratamientos oncológicos previos y la respuesta del tejido. La valoración médica previa es imprescindible para definir expectativas ajustadas a cada caso.", False),
    ("", False),
    # --- H2: Riesgos
    ("H2: Riesgos y posibles complicaciones", True),
    ("Como cualquier cirugía mayor, la reconstrucción mamaria conlleva riesgos que deben conocerse y evaluarse individualmente antes de tomar la decisión.", False),
    ("", False),
    ("Las posibles complicaciones incluyen:", False),
    ("", False),
    ("— Infección postoperatoria de la herida o del implante.", False),
    ("— Hematoma o seroma (acumulación de sangre o líquido en la zona intervenida).", False),
    ("— Necrosis parcial o total del colgajo (en técnicas con tejido propio).", False),
    ("— Contractura capsular (formación de tejido cicatricial duro alrededor del implante).", False),
    ("— Rotura del implante (poco frecuente con los implantes actuales de cohesive gel).", False),
    ("— Asimetría o resultado estético que requiera una cirugía correctora secundaria.", False),
    ("— Alteración de la sensibilidad en la zona reconstruida y en la zona donante.", False),
    ("— Cicatrices visibles, especialmente en técnicas con colgajo.", False),
    ("— Complicaciones anestésicas propias de toda cirugía mayor.", False),
    ("", False),
    ("H3: Impacto de la radioterapia previa en el resultado", True),
    ("La radioterapia previa sobre la zona del pecho es el factor de riesgo más relevante en la reconstrucción mamaria. El tejido irradiado tiene menor capacidad de cicatrización, irrigación reducida y mayor riesgo de contractura. En estos casos, las técnicas con tejido propio suelen ofrecer mejores resultados que las basadas en implantes, ya que aportan tejido bien vascularizado. La valoración médica individualizada es especialmente importante en este perfil de pacientes.", False),
    ("", False),
    # --- H2: Contraindicaciones
    ("H2: Contraindicaciones: cuándo puede no estar indicada la reconstrucción mamaria", True),
    ("Existen situaciones clínicas que pueden contraindicar o posponer la reconstrucción hasta que las condiciones sean más favorables.", False),
    ("", False),
    ("La reconstrucción puede no estar indicada o debe posponerse en pacientes con:", False),
    ("", False),
    ("— Tratamiento oncológico activo no finalizado (quimioterapia en curso, radioterapia activa), salvo decisión consensuada con el equipo oncológico.", False),
    ("— Radioterapia planificada postmastectomía que desaconseje la colocación de implantes.", False),
    ("— Enfermedades sistémicas no controladas: diabetes descompensada, inmunosupresión grave, insuficiencia cardiorrespiratoria.", False),
    ("— Tabaquismo activo: el tabaco compromete severamente la microcirculación y la cicatrización. Se recomienda un período mínimo de abstinencia antes de la cirugía.", False),
    ("— Estado nutricional deficiente que dificulte la recuperación.", False),
    ("— Expectativas no realistas o ausencia de motivación suficiente para afrontar una recuperación prolongada.", False),
    ("", False),
    ("La indicación definitiva y el momento óptimo se establecen siempre en coordinación con el equipo oncológico y tras una valoración médica individual completa.", False),
    ("", False),
    # --- H2: Qué NO es
    ("H2: Qué NO es la reconstrucción mamaria", True),
    ("Es importante entender con claridad qué no puede ofrecer este procedimiento para evitar expectativas inadecuadas que generen frustración.", False),
    ("", False),
    ("H3: No es una cirugía puramente estética", True),
    ("La reconstrucción mamaria es cirugía reparadora, no estética electiva. Su objetivo no es mejorar el aspecto de un pecho sano, sino restaurar la integridad corporal tras una mastectomía. Esto implica que los criterios de éxito son distintos: el objetivo no es la perfección estética, sino un resultado funcional, simétrico y compatible con el bienestar de la paciente.", False),
    ("", False),
    ("H3: No garantiza un resultado idéntico al pecho original", True),
    ("La reconstrucción mamaria puede ofrecer un resultado muy satisfactorio, pero no reproduce exactamente el pecho natural. La sensibilidad en la zona reconstruida puede ser parcial o diferente, la textura varía según la técnica, y las cicatrices son parte inevitable del proceso. El objetivo es un resultado armonioso, no una réplica perfecta.", False),
    ("", False),
    ("H3: No siempre es un proceso de una sola intervención", True),
    ("En la mayoría de los casos, la reconstrucción completa requiere al menos dos fases: la reconstrucción del volumen y, posteriormente, la reconstrucción del complejo areola-pezón. En algunos casos puede ser necesaria también una cirugía de simetría sobre el pecho contralateral. Es fundamental que la paciente entienda este proceso antes de comenzar.", False),
    ("", False),
    ("H3: No interfiere con el seguimiento oncológico", True),
    ("La reconstrucción mamaria no dificulta el seguimiento del cáncer de mama. El equipo de oncología adapta el protocolo de revisiones al nuevo contexto anatómico. La presencia de un implante no impide las revisiones periódicas, y las técnicas con tejido propio permiten también un seguimiento oncológico adecuado.", False),
    ("", False),
    # --- H2: Resultados
    ("H2: Resultados: qué esperar y qué NO esperar", True),
    ("El proceso completo puede requerir varios meses y más de una intervención; el resultado definitivo no se aprecia hasta que la cicatrización ha madurado.", False),
    ("", False),
    ("H3: Resultados inmediatos", True),
    ("Tras la cirugía, la paciente despertará con el pecho reconstruido, aunque todavía con inflamación, hematomas y en fase de cicatrización inicial. El resultado en este momento no refleja el resultado definitivo. Es habitual una sensación de tensión, pesadez o entumecimiento en la zona operada.", False),
    ("", False),
    ("H3: Resultados progresivos", True),
    ("La forma y el aspecto definitivo del pecho reconstruido se consolidan de forma gradual durante los meses siguientes, conforme desaparece el edema, maduran las cicatrices y el tejido se adapta. En casos con expansor tisular, el proceso completo puede extenderse entre 12 y 18 meses hasta llegar al resultado final.", False),
    ("", False),
    ("H3: Antes y después de la reconstrucción mamaria", True),
    ("Los resultados antes y después de la reconstrucción mamaria son variables y dependen de la técnica empleada, las características del tejido, los tratamientos oncológicos previos y la respuesta individual de cada paciente. No deben utilizarse casos ajenos como referencia directa del propio resultado esperado.", False),
    ("", False),
    ("Resultados variables según paciente. Las imágenes con fines informativos no son representativas del resultado individual.", False),
    ("", False),
    ("H3: Duración de los resultados", True),
    ("Los resultados obtenidos con tejido propio (colgajos) son generalmente permanentes, ya que el tejido trasplantado se integra como parte del cuerpo. Los resultados con implantes tienen larga duración, pero los implantes pueden requerir revisión, reposicionamiento o sustitución con el paso de los años, especialmente si se producen complicaciones como la contractura capsular.", False),
    ("", False),
    ("H3: Qué NO esperar", True),
    ("— Un resultado idéntico al pecho natural previo a la mastectomía.", False),
    ("— Recuperación completa de la sensibilidad en todos los casos.", False),
    ("— Resultado definitivo visible en las primeras semanas.", False),
    ("— Un único procedimiento en todos los casos.", False),
    ("— Resultados permanentes sin necesidad de seguimiento en técnicas con implante.", False),
    ("", False),
    # --- H2: Procedimiento
    ("H2: Procedimiento paso a paso: la experiencia en Diagonal CQ", True),
    ("El proceso comienza con la valoración médica y se adapta en todo momento al protocolo oncológico individual de cada paciente.", False),
    ("", False),
    ("[añadir imagen: consulta médica real de Diagonal CQ / Dr. Joan Benítez con paciente, sin rostros identificables]", False),
    ("", False),
    ("1. Valoración médica inicial: el Dr. Joan Benítez analiza el estado de la paciente, los informes oncológicos (tipo de mastectomía, radioterapia, quimioterapia), las características físicas y los objetivos para determinar qué técnica o combinación de técnicas es la más adecuada.", False),
    ("", False),
    ("2. Coordinación con el equipo oncológico: antes de programar la cirugía se confirma con el oncólogo el momento idóneo en función del protocolo de tratamiento. Esta coordinación es fundamental para garantizar la seguridad de la paciente.", False),
    ("", False),
    ("3. Planificación quirúrgica detallada: se explica a la paciente la técnica propuesta, las fases del proceso, los resultados esperados, los riesgos específicos y los cuidados postoperatorios. Se resuelven todas las dudas antes de confirmar la intervención.", False),
    ("", False),
    ("4. Intervención quirúrgica: se realiza en quirófano bajo anestesia general. La duración varía entre 2 y 8 horas según la complejidad de la técnica (menor tiempo en implante directo, mayor en técnicas con colgajos microquirúrgicos).", False),
    ("", False),
    ("5. Ingreso hospitalario: el ingreso habitual es de 1 a 5 días según la técnica empleada y la evolución postoperatoria.", False),
    ("", False),
    ("6. Seguimiento postoperatorio: revisiones programadas para valorar la cicatrización, el aspecto del resultado y detectar precozmente cualquier complicación.", False),
    ("", False),
    ("7. Segunda fase (si procede): reconstrucción del complejo areola-pezón mediante cirugía menor, tatuaje médico o combinación de ambos. Esta fase suele realizarse entre 3 y 6 meses después de la primera intervención, cuando el resultado inicial ha estabilizado.", False),
    ("", False),
    ("8. Cirugía de simetría contralateral (si procede): en algunos casos se propone también una intervención sobre la mama sana para mejorar la simetría global.", False),
    ("", False),
    # --- H2: Recuperación
    ("H2: Recuperación y cuidados postoperatorios", True),
    ("La recuperación varía según la técnica empleada y puede extenderse entre 4 y 10 semanas antes de la reincorporación plena a la actividad.", False),
    ("", False),
    ("H3: Primera semana", True),
    ("Reposo en cama con la cabecera elevada. Pueden colocarse drenajes para evitar la acumulación de líquido, que se retiran habitualmente entre el tercer y el quinto día. Dolor moderado controlable con analgesia prescrita. Movilidad limitada del brazo del lado operado.", False),
    ("", False),
    ("H3: Segunda a cuarta semana", True),
    ("Recuperación progresiva de la movilidad. Vuelta a actividades sedentarias (trabajo de oficina) a partir de la tercera o cuarta semana en técnicas con implante, y a partir de la quinta o sexta en técnicas con colgajo. Uso de sujetador quirúrgico o prenda de compresión según indicación. Cuidado de cicatrices con los productos recomendados por el equipo médico.", False),
    ("", False),
    ("H3: Segundo mes y seguimiento posterior", True),
    ("Reincorporación progresiva a la actividad física. Evitar esfuerzos importantes con los brazos y cargas pesadas hasta que el cirujano lo autorice. Fotoprotección estricta de las cicatrices durante al menos 12 meses para prevenir la hiperpigmentación. Revisiones periódicas según el calendario establecido por el Dr. Joan Benítez.", False),
    ("", False),
    ("Recomendaciones generales: no fumar durante todo el proceso (el tabaco es el principal factor de riesgo de complicaciones), hidratación adecuada, dieta equilibrada y seguir estrictamente las indicaciones médicas.", False),
    ("", False),
    # --- H2: Reconstrucción pezón
    ("H2: Reconstrucción del complejo areola-pezón", True),
    ("La reconstrucción del pezón y la areola es la fase final del proceso y completa el resultado estético de la reconstrucción mamaria.", False),
    ("", False),
    ("Existen varias opciones para reconstruir el complejo areola-pezón:", False),
    ("", False),
    ("— Reconstrucción quirúrgica del pezón: se crea el relieve del pezón mediante técnicas de colgajo local con la propia piel de la mama reconstruida. Es una intervención menor realizada habitualmente con anestesia local.", False),
    ("— Tatuaje médico de areola: el tatuaje médico permite recrear el color y el aspecto visual de la areola y, cuando no se ha reconstruido el relieve, también del pezón mediante técnicas de sombreado en 3D. Es la opción menos invasiva y la de recuperación más rápida.", False),
    ("— Combinación de ambas técnicas: en la mayoría de los casos se combina la reconstrucción quirúrgica del relieve del pezón con el tatuaje médico de la areola para obtener el resultado más natural posible.", False),
    ("", False),
    ("El momento de esta segunda fase se decide en función de la estabilización del resultado de la reconstrucción principal, habitualmente entre 3 y 6 meses después.", False),
    ("", False),
    # --- H2: Precio
    ("H2: Precio orientativo de la reconstrucción mamaria en Córdoba", True),
    ("El coste varía significativamente según la técnica, la complejidad del caso y si se realiza en uno o varios tiempos quirúrgicos.", False),
    ("", False),
    ("El precio de la reconstrucción mamaria depende de múltiples factores: la técnica quirúrgica empleada (implante directo, expansor, colgajo), si se realiza en uno o dos tiempos, la necesidad de cirugía de simetría contralateral, la complejidad del caso individual y el contexto oncológico.", False),
    ("", False),
    ("Es importante tener en cuenta que:", False),
    ("", False),
    ("— En la sanidad pública española, la reconstrucción mamaria por cáncer de mama está cubierta por el Sistema Nacional de Salud en virtud de la Ley 10/2010.", False),
    ("— En el ámbito privado, la mayoría de los seguros médicos con cobertura quirúrgica incluyen la reconstrucción mamaria. Es recomendable verificar las condiciones específicas de la póliza y solicitar el informe de indicación médica.", False),
    ("— Los precios orientativos en clínicas privadas de Córdoba para reconstrucción con implante oscilan entre 4.000 y 8.000 euros; con técnicas de colgajo, entre 8.000 y 16.000 euros, según el caso.", False),
    ("", False),
    ("Para obtener información sobre los precios en Diagonal CQ y estudiar la cobertura de tu seguro, puedes contactar con nosotros a través de nuestra página de contacto: https://diagonalcq.es/contacto. La información económica nunca condiciona la indicación clínica.", False),
    ("", False),
    # --- H2: Alternativas (before table)
    ("H2: Alternativas al tratamiento y técnicas complementarias", True),
    ("La elección de la técnica de reconstrucción más adecuada es una decisión médica personalizada que debe consensuarse con el cirujano plástico y el equipo oncológico.", False),
    ("", False),
]

# Tabla comparativa de técnicas
TABLE_HEADERS = ["Técnica", "Indicación principal", "Cicatriz adicional", "Recuperación aproximada", "Resultado a largo plazo"]
TABLE_ROWS = [
    ["Implante directo", "Cobertura cutánea suficiente, sin radioterapia prevista", "No", "3-4 semanas", "Bueno; puede requerir revisión del implante con los años"],
    ["Expansor + implante (2 tiempos)", "Cobertura insuficiente, sin radioterapia activa", "No", "6-12 meses (proceso)", "Bueno; requiere segunda intervención"],
    ["Colgajo DIEP (abdomen)", "Tejido abdominal disponible, radioterapia previa o rechazo a implantes", "Sí (abdomen)", "6-10 semanas", "Excelente; resultado permanente y natural"],
    ["Colgajo TRAM (abdomen)", "Tejido abdominal disponible, alternativa al DIEP", "Sí (abdomen)", "6-10 semanas", "Muy bueno; mayor impacto en zona donante que DIEP"],
    ["Colgajo dorsal ancho (espalda)", "Tejido dorsal disponible, combinable con implante", "Sí (espalda)", "5-8 semanas", "Bueno; habitualmente combinado con implante"],
    ["Técnica combinada", "Volumen insuficiente con tejido propio, radioterapia previa", "Sí (zona donante)", "6-10 semanas", "Muy bueno; aprovecha ventajas de ambas técnicas"],
]

BLOCKS_AFTER_TABLE = [
    ("", False),
    # --- H2: FAQ
    ("H2: Preguntas frecuentes sobre reconstrucción mamaria", True),
    ("", False),
    ("H3: ¿La reconstrucción mamaria la cubre la Seguridad Social?", True),
    ("Sí. La Ley 10/2010 de 9 de julio reconoce el derecho de toda paciente mastectomizada a la reconstrucción mamaria en el sistema sanitario público español. En el ámbito privado, la mayoría de los seguros médicos con cobertura quirúrgica también la incluyen. Es recomendable verificar las condiciones específicas de la póliza y solicitar el informe de indicación médica al especialista.", False),
    ("", False),
    ("H3: ¿Cuándo se puede realizar la reconstrucción mamaria?", True),
    ("Puede realizarse en el mismo acto quirúrgico que la mastectomía (reconstrucción inmediata) o en un momento posterior, una vez finalizado el tratamiento oncológico (reconstrucción diferida). Cuando se prevé radioterapia postoperatoria, generalmente se recomienda la reconstrucción diferida para evitar que la radiación comprometa el resultado. El momento idóneo se decide siempre en coordinación con el equipo de oncología.", False),
    ("", False),
    ("H3: ¿Cuánto tiempo dura la recuperación de la reconstrucción mamaria?", True),
    ("La recuperación varía según la técnica. Con implante directo, la reincorporación a actividades habituales suele producirse entre la tercera y la cuarta semana. Con técnicas de colgajo (DIEP, TRAM, dorsal ancho), la recuperación completa puede extenderse entre 6 y 10 semanas, aunque varía según cada paciente y el tipo de trabajo o actividad física que realice.", False),
    ("", False),
    ("H3: ¿Qué técnica de reconstrucción mamaria es mejor?", True),
    ("No existe una técnica universalmente mejor. La elección depende del perfil oncológico de la paciente, su anatomía, los tratamientos recibidos (especialmente la radioterapia), sus preferencias personales y su estado de salud general. El objetivo de la valoración médica es identificar la opción que ofrezca el mejor equilibrio entre resultado estético, seguridad y recuperación para cada caso concreto.", False),
    ("", False),
    ("H3: ¿Se puede hacer la reconstrucción mamaria años después de la mastectomía?", True),
    ("Sí. La reconstrucción diferida puede plantearse incluso años después de la mastectomía, siempre que el estado de salud general de la paciente lo permita y no existan contraindicaciones médicas. No hay un límite de tiempo establecido, aunque la calidad del tejido y el grado de fibrosis en la zona pueden influir en la elección de la técnica.", False),
    ("", False),
    ("H3: ¿La reconstrucción mamaria es dolorosa?", True),
    ("Como toda cirugía mayor, conlleva dolor postoperatorio, especialmente durante los primeros días. Este dolor se controla adecuadamente con la analgesia prescrita. En técnicas con colgajo, puede haber también molestias en la zona donante. A medida que avanza la recuperación, las molestias disminuyen progresivamente.", False),
    ("", False),
    ("H3: ¿Puedo dar el pecho después de una reconstrucción mamaria?", True),
    ("La reconstrucción mamaria unilateral no afecta a la lactancia por el pecho no intervenido. Sin embargo, el pecho reconstruido no tiene función glandular, por lo que no producirá leche. Si la paciente tiene intención de quedarse embarazada en el futuro, es importante comentarlo con el cirujano durante la planificación, ya que puede influir en la elección de la técnica.", False),
    ("", False),
    ("H3: ¿Es necesaria la reconstrucción del pezón y la areola?", True),
    ("No es obligatoria, pero sí la recomendada para la mayoría de las pacientes que desean un resultado estético completo. La reconstrucción del complejo areola-pezón es la fase final del proceso y puede realizarse mediante cirugía menor, tatuaje médico o una combinación de ambos. Muchas pacientes encuentran esta fase especialmente significativa desde el punto de vista emocional.", False),
    ("", False),
    # --- H2: Cuándo acudir
    ("H2: Cuándo acudir a un especialista en Córdoba", True),
    ("Si has sido diagnosticada de cáncer de mama, estás valorando una mastectomía preventiva o ya has sido mastectomizada y deseas conocer tus opciones de reconstrucción, lo más recomendable es solicitar una valoración médica especializada antes de tomar ninguna decisión.", False),
    ("", False),
    ("En Diagonal CQ, el Dr. Joan Benítez puede orientarte sobre las opciones disponibles en tu caso concreto, explicarte con honestidad qué resultados son realistas y coordinar la planificación con tu equipo oncológico si es necesario.", False),
    ("", False),
    ("Si resides en Córdoba, Sevilla o cualquier localidad cercana y quieres una primera consulta personalizada, puedes contactar con nosotros a través de: https://diagonalcq.es/contacto", False),
    ("", False),
    # --- Pie E-E-A-T
    ("Doctor responsable: Dr. Joan Benítez", False),
    ("Especialidad médica: Cirugía Plástica, Reparadora y Estética", False),
    ("Número de colegiado: 14/14/06121", False),
    ("Registro sanitario del centro: NICA 54005", False),
    ("", False),
    ("Artículo elaborado por el equipo médico de Diagonal CQ.", False),
    ("Revisado por el Dr. Joan Benítez, especialista en Cirugía Plástica, Reparadora y Estética, nº colegiado 14/14/06121.", False),
    ("Centro sanitario registrado con nº NICA 54005.", False),
    ("Última actualización: mayo de 2026.", False),
    ("", False),
    ("Este contenido es informativo y no sustituye una valoración médica presencial.", False),
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def utf16_len(text):
    return sum(2 if ord(c) > 0xFFFF else 1 for c in text)

def loc(idx):
    return {"index": idx, "tabId": TAB_ID}

def rng(start, end):
    return {"startIndex": start, "endIndex": end, "tabId": TAB_ID}

def preprocess_blocks(blocks):
    """Elimina líneas en blanco justo después de headings (is_bold=True)."""
    result = []
    skip_next_blank = False
    for text, is_bold in blocks:
        if skip_next_blank and text == "":
            skip_next_blank = False
            continue
        skip_next_blank = is_bold and text != ""
        result.append((text, is_bold))
    return result

def build_text_requests(blocks, start_index):
    """Returns (insert_requests, bold_ranges, bullet_ranges, blue_ranges, final_index)."""
    inserts = []
    bold_ranges = []
    bullet_ranges = []
    blue_ranges = []
    idx = start_index
    for text, is_bold in preprocess_blocks(blocks):
        is_bullet = text.startswith("— ")
        is_blue = text.startswith("[añadir imagen") or text.startswith("[AÑADIR IMAGEN")
        if is_bullet:
            text = text[2:]
        full = text + "\n"
        n = utf16_len(full)
        inserts.append({"insertText": {"location": loc(idx), "text": full}})
        if is_bold and text:
            bold_ranges.append((idx, idx + n))
        if is_bullet and text:
            bullet_ranges.append((idx, idx + n))
        if is_blue and text:
            blue_ranges.append((idx, idx + n))
        idx += n
    return inserts, bold_ranges, bullet_ranges, blue_ranges, idx

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
creds = get_google_credentials()
service = build("docs", "v1", credentials=creds)

# 1. Clear tab content
print("Leyendo documento...")
doc = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
end_index = 1
for tab in doc.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            end_index = max(1, body_content[-1].get("endIndex", 2) - 1)
        break

if end_index > 1:
    print(f"Limpiando contenido existente (índice 1 a {end_index})...")
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [{"deleteContentRange": {"range": rng(1, end_index)}}]},
    ).execute()
    print("Contenido anterior eliminado.")

# 2. Insert content BEFORE table (solo inserts + bullets, sin bold todavía)
print("Insertando contenido principal...")
ins_before, bold_before, bullet_before, blue_before, idx_after_before = build_text_requests(BLOCKS_BEFORE_TABLE, 1)
bullet_reqs_before = [
    {"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
    for s, e in bullet_before
]
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": ins_before + bullet_reqs_before},
).execute()
print(f"  Bloque 1 insertado. Indice actual: {idx_after_before}")

# 3. Insert the comparison table
table_position = idx_after_before
num_rows = len(TABLE_ROWS) + 1
num_cols = len(TABLE_HEADERS)
print(f"Insertando tabla ({num_rows} filas x {num_cols} columnas)...")
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"insertTable": {
        "rows": num_rows, "columns": num_cols, "location": loc(table_position),
    }}]},
).execute()

# 4. Re-read to find cell positions
print("Leyendo posiciones de celdas...")
doc2 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
target_table = None
for tab in doc2.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        for element in tab.get("documentTab", {}).get("body", {}).get("content", []):
            if "table" in element and abs(element.get("startIndex", 0) - table_position) <= 5:
                target_table = element["table"]
                break
        break

if target_table is None:
    print("ERROR: no se encontro la tabla.")
    sys.exit(1)

all_rows_data = [TABLE_HEADERS] + TABLE_ROWS
cell_requests = []
for r_idx, (row_el, row_data) in enumerate(zip(target_table.get("tableRows", []), all_rows_data)):
    for cell_el, cell_text in zip(row_el.get("tableCells", []), row_data):
        cell_content = cell_el.get("content", [])
        if cell_content:
            insert_idx = cell_content[0].get("startIndex", 0)
            cell_requests.append({"insertText": {"location": loc(insert_idx), "text": cell_text}})
            # Bold fila cabecera — se aplica aquí porque es dentro de la tabla
            if r_idx == 0:
                cell_requests.append({"updateTextStyle": {
                    "range": rng(insert_idx, insert_idx + utf16_len(cell_text)),
                    "textStyle": {"bold": True}, "fields": "bold",
                }})

service.documents().batchUpdate(documentId=DOC_ID, body={"requests": cell_requests}).execute()
print("  Tabla rellenada.")

# 5. Find new end index after table
doc3 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
new_end = 1
for tab in doc3.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            new_end = max(1, body_content[-1].get("endIndex", 2) - 1)
        break

# 6. Insert content AFTER table (solo inserts + bullets, sin bold todavía)
print("Insertando contenido despues de la tabla...")
ins_after, bold_after, bullet_after, blue_after, final_idx = build_text_requests(BLOCKS_AFTER_TABLE, new_end)
bullet_reqs_after = [
    {"createParagraphBullets": {"range": rng(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}}
    for s, e in bullet_after
]
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": ins_after + bullet_reqs_after},
).execute()
print(f"  Bloque 2 insertado. Indice final: {final_idx}")

# 7. Re-read and apply Arial 11 to everything
print("Aplicando Arial 11...")
doc4 = service.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
total_end = 1
for tab in doc4.get("tabs", []):
    if tab.get("tabProperties", {}).get("tabId") == TAB_ID:
        body_content = tab.get("documentTab", {}).get("body", {}).get("content", [])
        if body_content:
            total_end = max(1, body_content[-1].get("endIndex", 2) - 1)
        break
service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": [{"updateTextStyle": {
        "range": rng(1, total_end),
        "textStyle": {
            "weightedFontFamily": {"fontFamily": "Arial"},
            "fontSize": {"magnitude": 11, "unit": "PT"},
        },
        "fields": "weightedFontFamily,fontSize",
    }}]},
).execute()
print(f"  Arial 11 aplicado (1 a {total_end}).")

# 8. Aplicar BOLD a todos los headings — ÚLTIMO paso, no se puede sobreescribir
print("Aplicando negrita a headings...")
all_bold = bold_before + bold_after
bold_reqs = [
    {"updateTextStyle": {"range": rng(s, e), "textStyle": {"bold": True}, "fields": "bold"}}
    for s, e in all_bold
]
if bold_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": bold_reqs}).execute()
print(f"  {len(bold_reqs)} headings en negrita.")

# 9. Aplicar AZUL a líneas de imagen — ÚLTIMO paso
print("Aplicando color azul a recomendaciones de imagen...")
all_blue = blue_before + blue_after
blue_reqs = [
    {"updateTextStyle": {
        "range": rng(s, e),
        "textStyle": {"foregroundColor": {"color": {"rgbColor": {
            "red": 0.063, "green": 0.392, "blue": 0.784
        }}}},
        "fields": "foregroundColor",
    }}
    for s, e in all_blue
]
if blue_reqs:
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": blue_reqs}).execute()
print(f"  {len(blue_reqs)} lineas de imagen en azul.")

print("\nDocumento completado con exito.")
print(f"  URL: https://docs.google.com/document/d/{DOC_ID}/edit?tab={TAB_ID}")
