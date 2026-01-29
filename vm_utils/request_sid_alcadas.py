import os
import requests
import json

class RequestToken:
    def __init__(self, baseUrl, username, password, by_user=True) -> None:
        self._baseUrl = baseUrl
        self._username = username
        self._password = password
        self._by_user = by_user
        self._token_response = None
        self._token_status = 400

    def _generate_token_by_user(self):
        # Cria uma primeira chamada ao SID para gerar um token de acesso
        urlToken = self._baseUrl + "/SASLogon/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password
        }

        authToken = ("sas.cli", "")

        try:
            response = requests.post(
                urlToken,
                data=data,
                headers=headers,
                verify=False,
                auth=authToken,
                timeout=1000
            )

            if response.status_code == 200:

                print(response.json())


                self._token_response = response.json()["access_token"]
                self._token_status = response.status_code
            else:
                self._token_response = response.json()
                self._token_status = response.status_code

        except requests.exceptions.RequestException as e:
            self._token_response = e

    def _generate_token_by_client(self):
        # Cria uma primeira chamada ao SID para gerar um token de acesso
        urlToken = self._baseUrl + "/SASLogon/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self._username,
            "client_secret": self._password
        }

        try:
            response = requests.post(
                urlToken,
                data=data,
                headers=headers,
                verify=False,
                timeout=1000
            )

            if response.status_code == 200:
                self._token_response = response.json()["access_token"]
                self._token_status = response.status_code
            else:
                self._token_response = response.json()
                self._token_status = response.status_code

        except requests.exceptions.RequestException as e:
            self._token_response = e

    def return_token(self):
        if self._by_user:
            self._generate_token_by_user()
        else:
            self._generate_token_by_client()          

        # print(f"token_response {self._token_response}")
        # print(f"token_status {self._token_status}")

        return (self._token_response, self._token_status)

class RequestSID:
  def __init__(self, base_url, token, decision_name, input_list) -> None:
    # Classe para criar chamadas aos fluxos publicados no SID
    self._base_url = base_url
    self._token = token
    self._decision_name = decision_name
    self._input_list = input_list
    self._sid_response = None
    self._sid_status = 400

  def _prepare_json(self, sid_response):
    """Funcao que transforma o response do SID em um json e adiciona os headers passados para o tradutor"""
    prepared_response = {}

    if sid_response.get("outputs"):
      for output in sid_response.get("outputs"):
        prepared_response[output.get("name")] = output.get("value")
    else:
      return sid_response

    return prepared_response

  def _call_decision(self):
    # Cria chamada para o fluxo passado em decision_name
    # As variáveis devem ser passadas para o input_list

    if self._token:
      urlSID = f"{self._base_url}/microanalyticScore/modules/{self._decision_name}/steps/execute"

      headersSID = {
        "Content-Type": "application/json;charset=utf-8",
        "Accept": "application/json",
        "Authorization": "Bearer " + self._token
      }

      bodySID = {
        "inputs": self._input_list
      }

      try:
        response = requests.post(
          urlSID,
          data=json.dumps(bodySID, ensure_ascii=False),
          headers=headersSID,
          verify=False,
          timeout=1000
        )

        print(response.json())

        self._sid_response = self._prepare_json(response.json())
        self._sid_status = response.status_code

      except requests.exceptions.RequestException as e:
        self._sid_response = e
    else:
      self._sid_response = "Erro no token: não foi possível realizar a chamada"

  def check_decision_name(self, decision_name_list):
    check = True if self._decision_name in decision_name_list else False

    return check

  def return_sid(self):
    self._call_decision()

    print(f"sid_response {self._sid_response}")
    print(f"sid_status {self._sid_status}")

    return (self._sid_response, self._sid_status)

def execute(base_url, username, password, decision_name, input_list):
  request_tk = RequestToken(base_url, username, password, by_user=True)
  tk_response, tk_status = request_tk.return_token()

  print(f"TOKEN status: {tk_status}")
  print(f"TOKEN response: {tk_response}")

  if not tk_response or tk_status != 200:
    print(f"could not create tk_response entity!")
    return {"token_status": tk_status, "token_response": tk_response}

  request_sid = RequestSID(base_url, tk_response, decision_name, input_list)
  sid_response, sid_status = request_sid.return_sid()

  print(f"\n\nbase_url: {base_url}/microanalyticScore/modules/{decision_name}/steps/execute")
  print(f"SID status: {sid_status}")
  print(f"SID response: {sid_response}")

  if not sid_response or sid_status != 201:
    print(f"could not create SID entity!")
    return {"sid_status": sid_status, "sid_response": sid_response}

  return {"sid_status": sid_status, "sid_response": sid_response}

if __name__ == "__main__":

    env_url = "pmdsas.aks.santanderbr.pre.corp"
    base_url = f"https://{env_url}"

    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']

    decision_name = "alcadas_decision_3"

    input_list = [
        {
          "name": "entradas_",
          "value": """{
            "GARANTIAS_QTD":"0001",
            "INTERVENIENTES_QTD":"0001",
            "CULT_AGRO_QTD":"0000",
            "LIN_LIMITE_QTD":"0002",
            "LIN_CONSUMO_QTD":"0064",
            "LST_ALCADAS_QTD":"0010",
            "TIP_CHAMADA":"2",
            "COD_ENTIDADE":"0033",
            "COD_CENTRO":"6408",
            "ANO_PROP":"2023",
            "NUM_PROP":"00000079",
            "DT_HR_CHAMADA":"2023-06-28-12.45.02.801805",
            "DT_PROPOSTA":"2023-06-28",
            "TIP_PROP_GARRA":"001",
            "COD_PROCESSO":"003",
            "PENUMPER":"00023573",
            "NR_DOCUM":"46395000000139",
            "PENUMGRU":"90193994",
            "COD_PRODUTO":"30",
            "COD_SUBPROD":"2022",
            "PRZ_PROPOSTA":"2013",
            "VLR_PROPOSTA":"00000000013000000",
            "VLR_RISCO_CLIE":"00000001050500000",
            "VLR_RISCO_GRP":"00000001050500000",
            "TIP_GRAU_SEVE":"3",
            "TIP_SCAN":"00",
            "QTD_DIAS_ATRAS":"0000",
            "COD_SEGM_PROP":"017",
            "COD_SEGM_PRIM":"017",
            "COD_SEGM_SEC":"037",
            "COD_ATVD_CNAE":"08411600",
            "COD_RATING":"65",
            "VLR_VALORACAO":"65",
            "COD_REDE":"6394",
            "COD_REGIONAL":"9088",
            "COD_CART_RISC":"",
            "COD_OUTROS_IND":"",
            "COD_SUCURSAL":"9998",
            "FAM_GAR_ALCADA":"AVA",
            "FAM_PROD_GARRA":"EM",
            "COD_CLA_USUA":"M12",
            "COD_ACAO_USUA":"035",
            "COD_BANCO_CONTR":"",
            "COD_AGENC_CONTR":"",
            "NUM_CONTR_ALTAIR":"",
            "FLAG_TAXA":"",
            "FLAG_PRAZO":"",
            "FLAG_VALOR":"",
            "FLAG_INTERV":"",
            "FLAG_TIT":"",
            "FLAG_GAR":"",
            "VL_CTR_ADT":"000000000000000",
            "SL_DEV_CTR_ADT":"000000000000000",
            "QT_TOT_PARC_CTR_ADT":"",
            "QT_PARC_PG_CTR_ADT":"",
            "VL_PARC_CTR_ADT":"000000000000000",
            "PRZ_ATU_OPER_ADT":"",
            "CMT_FILA":"6110",
            "NIV_USUA_FILA":"215",
            "NIV_CENT_FILA":"110",
            "CMT_DEVOL":"",
            "NIV_USUA_DEVOL":"",
            "NIV_CENT_DEVOL":"",
            "SIG_USUA_DEVOL":"",
            "CMT_ENCAM":"",
            "NIV_USUA_ENCAM":"",
            "NIV_CENT_ENCAM":"",
            "SIG_USUA_ENCAM":"",
            "CMT_ALC_ATU":"6110",
            "NIV_USUA_ALC_ATU":"215",
            "NIV_CENT_ALC_ATU":"110",
            "COD_USUARIO_CLAS":"T682215 ",
            "COD_AGRUPACI_1":"",
            "VLR_RISCO_1":"000000000000000",
            "COD_AGRUPACI_2":"",
            "VLR_RISCO_2":"000000000000000",
            "COD_AGRUPACI_3":"",
            "VLR_RISCO_3":"000000000000000",
            "COD_AGRUPACI_4":"",
            "VLR_RISCO_4":"000000000000000",
            "COD_AGRUPACI_5":"",
            "VLR_RISCO_5":"000000000000000",
            "COD_AGRUPACI_6":"",
            "VLR_RISCO_6":"000000000000000",
            "COD_AGRUPACI_7":"",
            "VLR_RISCO_7":"000000000000000",
            "COD_AGRUPACI_8":"",
            "VLR_RISCO_8":"000000000000000",
            "COD_AGRUPACI_9":"",
            "VLR_RISCO_9":"000000000000000",
            "COD_AGRUPACI_10":"",
            "VLR_RISCO_10":"000000000000000",
            "COD_AGRUPACI_11":"",
            "VLR_RISCO_11":"000000000000000",
            "COD_AGRUPACI_12":"",
            "VLR_RISCO_12":"000000000000000",
            "COD_AGRUPACI_13":"",
            "VLR_RISCO_13":"000000000000000",
            "COD_AGRUPACI_14":"",
            "VLR_RISCO_14":"000000000000000",
            "COD_AGRUPACI_15":"",
            "VLR_RISCO_15":"000000000000000",
            "COD_AGRUPACI_16":"",
            "VLR_RISCO_16":"000000000000000",
            "COD_AGRUPACI_17":"",
            "VLR_RISCO_17":"000000000000000",
            "COD_AGRUPACI_18":"",
            "VLR_RISCO_18":"000000000000000",
            "COD_AGRUPACI_19":"",
            "VLR_RISCO_19":"000000000000000",
            "COD_AGRUPACI_20":"",
            "VLR_RISCO_20":"000000000000000",
            "PRZ_CAREN":"",
            "TIP_CAREN":"",
            "RSCD_1":"",
            "PRDD_1":"0000",
            "RSCD_2":"",
            "PRDD_2":"0000",
            "RSCD_3":"",
            "PRDD_3":"0000",
            "IND_P2NIVEL":"N",
            "QTD_DISP_BYP_2N":"000",
            "QTD_DISP_BYP_CHK":"000",
            "COD_CAMPANHA":"00000",
            "GARANTIAS":"998::S::S::100000000::;",
            "INTERVENIENTES":"00023573::TI::100000000:: ::00023573;",
            "CULT_AGRO":"",
            "LIN_LIMITE":"P::00023573;G::90193994;",
            "LIN_CONSUMO":"001::LM000::000000050000000::000000013500000::1001;001::A0001::000000000000000::000000000000000::1370;001::A0002::000000010000000::000000000000000::1730;001::A0003::000000000000000::000000000000000::2036;001::A0004::000000000000000::000000007500000::2048;001::A0005::000000000000000::000000000000000::2060;001::A0006::000000050000000::000000006000000::1100;001::A0007::000000000000000::000000000000000::1190;001::G0001::000000000000000::000000000000000::1001;001::G0002::000000000000000::000000000000000::1001;001::G0003::000000010000000::000000000000000::1001;001::G0004::000000000000000::000000000000000::1001;001::G0005::000000000000000::000000000000000::1001;001::G0006::000000000000000::000000000000000::1001;001::G0007::000000000000000::000000000000000::1001;001::G0008::000000000000000::000000000000000::1001;001::G0009::000000050000000::000000000000000::1001;001::G0010::000000000000000::000000000000000::1001;001::G0012::000000000000000::000000000000000::1001;001::G0013::000000000000000::000000000000000::1001;001::G0014::000000000000000::000000000000000::1001;001::G0015::000000000000000::000000000000000::1001;001::G9998::000000050000000::000000013500000::1001;001::M0001::000000050000000::000000013500000::1800;001::M0002::000000000000000::000000000000000::1800;001::P0001::000000000000000::000000000000000::1370;001::P0002::000000010000000::000000000000000::1730;001::P0003::000000000000000::000000000000000::2036;001::P0004::000000000000000::000000007500000::2048;001::P0005::000000000000000::000000000000000::2060;001::P0006::000000050000000::000000006000000::1100;001::P0007::000000000000000::000000000000000::1190;002::LM000::000000050000000::000000013500000::1180;002::A0001::000000000000000::000000000000000::1370;002::A0002::000000010000000::000000000000000::1730;002::A0003::000000000000000::000000000000000::2036;002::A0004::000000000000000::000000007500000::2048;002::A0005::000000000000000::000000000000000::2060;002::A0006::000000050000000::000000006000000::1100;002::A0007::000000000000000::000000000000000::1190;002::G0001::000000000000000::000000000000000::1001;002::G0002::000000000000000::000000000000000::1001;002::G0003::000000010000000::000000000000000::1001;002::G0004::000000000000000::000000000000000::1001;002::G0005::000000000000000::000000000000000::1001;002::G0006::000000000000000::000000000000000::1001;002::G0007::000000000000000::000000000000000::1001;002::G0008::000000000000000::000000000000000::1001;002::G0009::000000050000000::000000000000000::1001;002::G0010::000000000000000::000000000000000::1001;002::G0012::000000000000000::000000000000000::1001;002::G0013::000000000000000::000000000000000::1001;002::G0014::000000000000000::000000000000000::1001;002::G0015::000000000000000::000000000000000::1001;002::G9998::000000050000000::000000013500000::1001;002::M0001::000000050000000::000000013500000::1001;002::M0002::000000000000000::000000000000000::1001;002::P0001::000000000000000::000000000000000::1370;002::P0002::000000010000000::000000000000000::1730;002::P0003::000000000000000::000000000000000::2036;002::P0004::000000000000000::000000007500000::2048;002::P0005::000000000000000::000000000000000::2060;002::P0006::000000050000000::000000006000000::1100;002::P0007::000000000000000::000000000000000::1190;",
            "LST_ALCADAS":"6408::307::177:: :: ::E;6110::215::110:: ::S::E;7117::311::182:: :: ::E;8919::270::140:: :: ::E;6955::272::137:: :: ::E;7594::285::155:: :: ::E;8965::273::138:: :: ::E;6956::280::150:: :: ::E;6954::290::160:: :: ::E;8558::295::165:: :: ::E;",
            "PE_IND_RAMO_SENSIVEL":"0",
            "LL_IND_RAMO_SENSIVEL":"0",
            "VL_LIM_CHQ":0,
            "VL_LIM_CAR":0,
            "VLR_HIST_APROV":[],
            "varsSaidaSegundoNivel":{
                "ret_indSegNivelOk":"N",
                "ret_decisaoPo2N":"SD",
                "ret_indByp2N":"",
                "ret_indBypChk":"",
                "ret_codParecer":"00001",
                "ret_vlrAprovAm":"0",
                "ret_przAprovAm":"0",
                "ret_garantiasAM":"0",
                "ret_siglaUsuAut":"",
                "ret_codMotivoNA":"",
                "listaDecisaoSegundoNivel":"[]"
            }
          }"""
        }
    ]

    # input_list = [
    #     {
    #       "name": "entradas_",
    #       "value": """{"GARANTIAS_QTD":"0000","INTERVENIENTES_QTD":"0001","CULT_AGRO_QTD":"0000","LIN_LIMITE_QTD":"0000","LIN_CONSUMO_QTD":"0000","LST_ALCADAS_QTD":"0011","TIP_CHAMADA":"2","COD_ENTIDADE":"0033","COD_CENTRO":"8033","ANO_PROP":"2024","NUM_PROP":"00138972","DT_HR_CHAMADA":"2024-01-19-13.30.40.628099","DT_PROPOSTA":"2024-01-19","TIP_PROP_GARRA":"001","COD_PROCESSO":"001","PENUMPER":"40233299","NR_DOCUM":"02705189000143","PENUMGRU":"90154398","COD_PRODUTO":"30","COD_SUBPROD":"2012","PRZ_PROPOSTA":"2060","VLR_PROPOSTA":"00000000025431446","VLR_RISCO_CLIE":"00000000063787334","VLR_RISCO_GRP":"00000000105046221","TIP_GRAU_SEVE":"9","TIP_SCAN":"99","QTD_DIAS_ATRAS":"0000","COD_SEGM_PROP":"011","COD_SEGM_PRIM":"011","COD_SEGM_SEC":"080","COD_ATVD_CNAE":"06491300","COD_RATING":"40","VLR_VALORACAO":"24","COD_REDE":"6241","COD_REGIONAL":"8040","COD_CART_RISC":"    ","COD_OUTROS_IND":"   ","COD_SUCURSAL":"9996","FAM_GAR_ALCADA":"AVA","FAM_PROD_GARRA":"RW","COD_CLA_USUA":"M07","COD_ACAO_USUA":"   ","COD_BANCO_CONTR":"    ","COD_AGENC_CONTR":"    ","NUM_CONTR_ALTAIR":"            ","FLAG_TAXA":" ","FLAG_PRAZO":" ","FLAG_VALOR":" ","FLAG_INTERV":" ","FLAG_TIT":" ","FLAG_GAR":" ","VL_CTR_ADT":"000000000000000","SL_DEV_CTR_ADT":"000000000000000","QT_TOT_PARC_CTR_ADT":"    ","QT_PARC_PG_CTR_ADT":"    ","VL_PARC_CTR_ADT":"000000000000000","PRZ_ATU_OPER_ADT":"    ","CMT_FILA":"8033","NIV_USUA_FILA":"001","NIV_CENT_FILA":"100","CMT_DEVOL":"    ","NIV_USUA_DEVOL":"   ","NIV_CENT_DEVOL":"   ","SIG_USUA_DEVOL":"        ","CMT_ENCAM":"    ","NIV_USUA_ENCAM":"   ","NIV_CENT_ENCAM":"   ","SIG_USUA_ENCAM":"        ","CMT_ALC_ATU":"8033","NIV_USUA_ALC_ATU":"001","NIV_CENT_ALC_ATU":"100","COD_USUARIO_CLAS":"T740669 ","COD_AGRUPACI_1":"     ","VLR_RISCO_1":"000000000000000","COD_AGRUPACI_2":"     ","VLR_RISCO_2":"000000000000000","COD_AGRUPACI_3":"     ","VLR_RISCO_3":"000000000000000","COD_AGRUPACI_4":"     ","VLR_RISCO_4":"000000000000000","COD_AGRUPACI_5":"     ","VLR_RISCO_5":"000000000000000","COD_AGRUPACI_6":"     ","VLR_RISCO_6":"000000000000000","COD_AGRUPACI_7":"     ","VLR_RISCO_7":"000000000000000","COD_AGRUPACI_8":"     ","VLR_RISCO_8":"000000000000000","COD_AGRUPACI_9":"     ","VLR_RISCO_9":"000000000000000","COD_AGRUPACI_10":"     ","VLR_RISCO_10":"000000000000000","COD_AGRUPACI_11":"     ","VLR_RISCO_11":"000000000000000","COD_AGRUPACI_12":"     ","VLR_RISCO_12":"000000000000000","COD_AGRUPACI_13":"     ","VLR_RISCO_13":"000000000000000","COD_AGRUPACI_14":"     ","VLR_RISCO_14":"000000000000000","COD_AGRUPACI_15":"     ","VLR_RISCO_15":"000000000000000","COD_AGRUPACI_16":"     ","VLR_RISCO_16":"000000000000000","COD_AGRUPACI_17":"     ","VLR_RISCO_17":"000000000000000","COD_AGRUPACI_18":"     ","VLR_RISCO_18":"000000000000000","COD_AGRUPACI_19":"     ","VLR_RISCO_19":"000000000000000","COD_AGRUPACI_20":"     ","VLR_RISCO_20":"000000000000000","PRZ_CAREN":"    ","TIP_CAREN":"  ","RSCD_1":"  ","PRDD_1":"0000","RSCD_2":"  ","PRDD_2":"0000","RSCD_3":"  ","PRDD_3":"0000","IND_P2NIVEL":"N","QTD_DISP_BYP_2N":"000","QTD_DISP_BYP_CHK":"000","COD_CAMPANHA":"     ","VLR_ENTRADA_BEM":0,"VLR_MERCADO_BEM_VEIC":0,"VLR_BEM_EQUIP":0,"COD_TIPO_BEM":"   ","ANO_FABRIC_BEM":"    ","GARANTIAS":"","INTERVENIENTES":"40233299::TI::100000000:: ::40233299;","CULT_AGRO":"","LIN_LIMITE":"","LIN_CONSUMO":"","LST_ALCADAS":"8033::001::100:: ::S::N;8033::205::100:: ::S::E;7681::215::110:: ::S::E;7116::245::115:: :: ::E;6116::270::140:: :: ::E;6115::272::137:: :: ::E;7594::285::155:: :: ::E;8965::273::138:: :: ::E;6956::280::150:: :: ::E;6954::290::160:: :: ::E;8558::295::165:: :: ::E;","PE_IND_RAMO_SENSIVEL":9,"LL_IND_RAMO_SENSIVEL":"0","VL_LIM_CHQ":"75815.0000","VL_LIM_CAR":"40000.0000","VLR_HIST_APROV":"[]","BG_QTDDIASTEMPOCONTAMENSAL":0,"PE_FAT_MED_MENSAL":0,"PE_FAT_ANUAL":0,"PE_FAT_PRESUMIDO":0,"PE_FAT_IMPOSTO":0,"PE_FLG_SINAL_ALERTA":"","ADT_VLR_TOT_VENCER":0}"""
    #     }
    # ]


    execute(base_url, username, password, decision_name, input_list)