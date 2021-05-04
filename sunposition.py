import numpy as np
import pandas as pd
from pysolar import solar

class Sunposition():
    '''
    '''
    def __init__(self, local_timezone, date_str, lat_lon):
        '''
        Parameters
        ==========
        local_timezone : str
        date_str : str, length == 8
            YYYMMDD format
        lat_lon : tuple, length == 2
        '''
        self.local_timezone = local_timezone
        self.date_str = f'{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}'
        self.lat, self.lon = lat_lon
        self.sunposition_df = self._init_dataframe()

    def _init_dataframe(self):
        df = pd.DataFrame()
        df = self._add_localtime_to_df(df=df)
        df = self._add_utctime_to_df(df=df)
        df = self._add_sunposition_to_df(df=df)
        df = self._drop_nonsunlit_rows(df=df)
        return df

    def _add_localtime_to_df(self, df):
        '''
        '''
        df['local_timestamps'] = pd.date_range(
            start=self.date_str + ' 00:00', 
            freq='15min', periods=96, tz=self.local_timezone
        )
        return df

    def _add_utctime_to_df(self, df):
        '''
        '''
        #df['utc_timestamps'] = df['local_timestamps'].tz_convert('UTC')
        df['utc_timestamps'] = pd.to_datetime(
            df['local_timestamps']).dt.tz_convert('UTC')
        return df

    def _add_sunposition_to_df(self, df):
        '''
        '''
        dts = pd.to_datetime(
            df['utc_timestamps'], infer_datetime_format=True,
        )
        df['altitude'] = [
            90 - solar.get_altitude(self.lat, self.lon, utc_dt) 
            for utc_dt in dts
        ]
        df['azimuth'] = [
            solar.get_azimuth(self.lat, self.lon, utc_dt) for utc_dt in dts
        ]
        return df

    @staticmethod
    def _drop_nonsunlit_rows(df):
        '''
        '''
        return df[df['altitude'] < 90]