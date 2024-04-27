from project_data.main_data import ProjectType


class DataTypesErrorExceptions:
    DATA = [['gps', 'SKU_SAP_CODE'],
            ['routes', 'code_plant'],
            ['routes', 'id_sh#point1'],
            ['sourcing_parameters', 'parameter value'],
            ['milk_parameters', 'parameter value'],
            ['rejections', 'date id']]


class ExcludeValidateColumns:
    __excluded = {
        ProjectType.PROMO: {
            'gps': ['SKU_SAP_CODE'],
            'prod_md': ['SKU_SAP_CODE']
        },
        ProjectType.RTM: {
            'fin_log_model': ['CD_LOG_SHIPPING_TYPE_HEADER'],
            'distance_data': ['ShipToID'],
            'wms_support': ['Номер клиента', 'Номер заказа']
        },
        ProjectType.TETRIS: {
            'parameters': ['Parameter ID', 'Parameter Value'],
            'plants': ['Location Code'],
            'warehouses': ['Location Code'],
            'rejections': ['Date ID']
        },
        ProjectType.CFR: {
            'routes': ['Code Plant', 'ID_Sh#point1'],
        }
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__excluded[optimizer_type]
