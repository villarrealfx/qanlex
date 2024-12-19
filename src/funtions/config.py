
# Configuración General

URL = 'https://scw.pjn.gov.ar/scw/home.seam'

# Variables 
select_jurid = '10'
tex_parte = 'RESIDUOS'



# Identificadores ID

ID_FORM_PUBLICA = 'formPublica:porParte:header:inactive'
ID_JURIDICCION = 'formPublica:camaraPartes'
ID_PARTE = 'formPublica:nomIntervParte'
ID_BUSCAR = 'formPublica:buscarPorParteButton'
ID_EXPEDIENTE_JURI = 'expediente:j_idt90:detailCamera'
ID_EXPEDIENTE_DEPE = 'expediente:j_idt90:detailDependencia'
ID_EXPEDIENTE_SITU = 'expediente:j_idt90:detailSituation'
ID_EXPEDIENTE_CARA = 'expediente:j_idt90:detailCover'
ID_INTERVINIENTES = 'expediente:j_idt261:header:inactive'



# XPATH

XP_RECAPCHA = '//*[@id="recaptcha-anchor"]/div[1]'
XP_DATATABLE = '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr'
XP_DATATABLE_COLUM = '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[1]/td'
XP_EXPEDIENTE = '//*[@id="expediente:j_idt90:j_idt91"]/div/div[1]/div/div/div[2]/span'
XP_PAGINACION_TEXTO_SIG = '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]/span'
XP_PAGINACION_BTN_SIG = '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]'
XP_PARTICIPANTES = '//*[@id="expediente:participantsTable"]/tbody[contains(@class,"rf-dt-b")]'
XP_RECAPCHA_ = '//*[@id="recaptcha-anchor"]'
XP_ACTUACIONES_FILAS = '//*[@id="expediente:action-table"]/tbody/tr'
XP_ACTUACIONES_COLUM = '//*[@id="expediente:action-table"]/tbody/tr[1]/td'