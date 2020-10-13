from keys import keys

refrigerators = {
    'storeId': '0',
    'device_list': [
        {'deviceId': 'a',
         'columns': 8,
         'ips': {
            '1':{
                'floor' : 0,
                'cameras' : ['l'],
                'camera_brightenss': 0.5
                },
            '2':{
                'floor' : 1,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '3':{
                'floor' : 2,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '4':{
                'floor' : 3,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '5':{
                'floor' : 4,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '6':{
                'floor' : 5,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            }
        },
        {'deviceId': 'b',
         'columns': 8,
         'ips': {
            '7': {
                'floor' : 0,
                'cameras' : ['l'],
                'camera_brightenss': 0.7
                },   
            '8': {
                'floor' : 1,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '9': {
                'floor' : 2,
                'cameras' : ['l'],
                'camera_brightenss': 0.7
                },
            '10': {
                'floor' : 3,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '11': {
                'floor' : 4,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '12': {
                'floor' : 5,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            }
        },
        {'deviceId': 'c',
         'columns': 8,
         'ips': {
            '13': {
                'floor' : 0,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },    
            '14': {
                'floor' : 1,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '15': {
                'floor' : 2,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '16': {
                'floor' : 3,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '17': {
                'floor' : 4,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            '18': {
                'floor' : 5,
                'cameras' : ['l'],
                'camera_brightenss': 0.3
                },
            }
        },
        {'deviceId': 'd',
         'columns': 8,
         'ips': {
            '19': {
                'floor' : 0,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },   
            '20': {
                'floor' : 1,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '21': {
                'floor' : 2,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '22': {
                'floor' : 3,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '23': {
                'floor' : 4,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '24': {
                'floor' : 5,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            }
        },        
        {'deviceId': 'e',
         'columns': 8,
         'ips': {
            '25': {
                'floor' : 0,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '26': {
                'floor' : 1,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '27': {
                'floor' : 2,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '28': {
                'floor' : 3,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '29': {
                'floor' : 4,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            '30': {
                'floor' : 5,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.5
                },
            }
        },        
        {'deviceId': 'f',
         'columns': 8,
         'ips': {
            '31': {
                'floor' : 0,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '32': {
                'floor' : 1,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.75
                },
            '33': {
                'floor' : 2,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '34': {
                'floor' : 3,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '35': {
                'floor' : 4,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            '36': {
                'floor' : 5,
                'cameras' : ['l', 'r'],
                'camera_brightenss': 0.3
                },
            }
        }
    ]
}

redis_info = {
    'host': '',
    'port': 6379,
    'db': 2,
    'username': 'worker',
    'password': keys.get('redis', './keys')
}


cam_info = {
    'MJPG_CODEC': 1196444237.0,
    'FHD_resolution' : {'width' : 1920, 'height' : 1080},
    '4k_resolution' : {'width' : 3264, 'height' : 2448}


}

netsork_info = {
    'base_url' : 'http://192.168.0.'

}

loadcell_info = {
    'baudrate' : 38400,
    'calibration_path' : './lc_cali.json'
}
