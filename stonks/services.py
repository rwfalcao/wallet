import json

from requests import request as api_request

class AlphaVantageWrapper:

    API_URL = 'https://www.alphavantage.co/query'
    API_KEY = 'P19FG0MB5JCPC7CO'

    def _requisicao(self, method, params=None):
        '''
            Função padrão para uso da library request
        '''
        headers = {}
        url = self.API_URL

        if method == 'GET':
            return api_request(
                method=method, 
                url=url, 
                params=params, 
                headers=headers, 
                verify=False)
        return None

    
    def get_daily_time_series(self, symbol):
        '''
            Retorna JSON com dados por dia de determinado símbolo.
        '''
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.API_KEY
        }

        response = self._requisicao(method='GET', params=params)

        return json.loads(response.content) if response.status_code == 200 else None