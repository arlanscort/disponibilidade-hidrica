import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'grib',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': 'total_precipitation',
        'year': '2023',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10',
        ],
        'area': [
            -26, -51, -28,
            -49,
        ],
        'time': '00:00',
    },
    'download.grib')