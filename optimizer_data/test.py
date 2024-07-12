from optimizer_data.operations import Operations
from project_data.main_data import ProjectType


class Test:

    @staticmethod
    def input_validation(optimizer_type: str, environment: str, delete_scenario_after_test: bool = True):

        operation = Operations(optimizer_type, environment)

        operation.change_active_project()
        operation.create_scenario()
        operation.upload_invalid_input_files()
        operation.errors_logs_comparison()

        if delete_scenario_after_test:
            operation.delete_scenario()

    @staticmethod
    def input_validation_all_optimizer(environment: str):
        optimizer_types = [ProjectType.PROMO, ProjectType.RTM, ProjectType.TETRIS, ProjectType.CFR]

        for optimizer_type in optimizer_types:
            print('INPUT VALIDATION:', optimizer_type.upper(), end='\n')
            Test.input_validation(optimizer_type, environment)
            print()

    @staticmethod
    def check_validation_rules(optimizer_type: str, use_last_created_file: bool = False):

        operation = Operations(optimizer_type)
        operation.validation_rules_comparison(use_last_created_file)

    @staticmethod
    def check_all_validation_rules(use_last_created_file: bool = False):
        optimizer_types = [ProjectType.PROMO, ProjectType.RTM, ProjectType.TETRIS, ProjectType.CFR]

        for optimizer_type in optimizer_types:
            print('CHECK VALIDATION RULES:', optimizer_type.upper(), end='\n')
            Test.check_validation_rules(optimizer_type, use_last_created_file)
            print()

    @staticmethod
    def create_scenario_and_filling_full_data(optimizer_type: str, environment: str, creating_scenario_data: dict = None):

        operation = Operations(optimizer_type, environment)

        operation.change_active_project()
        operation.create_scenario(creating_scenario_data)
        operation.upload_valid_input_files()
        operation.save_defoult_scenario_pfr()

    @staticmethod
    def create_scenario_and_filling_downloaded_data(optimizer_type: str,
                                                    environment: str,
                                                    zip_dir: str,
                                                    creating_scenario_data: dict = None):

        operation = Operations(optimizer_type, environment)

        operation.change_active_project()
        operation.create_scenario(creating_scenario_data)
        operation.upload_downloaded_input_files(zip_dir)
        operation.save_defoult_scenario_pfr()

    @staticmethod
    def fill_new_scenario_and_calculate(optimizer_type: str,
                                        environment: str,
                                        creating_scenario_data: dict = None,
                                        not_download_input_list: list = None,
                                        valid_input_files_folder: str = None,
                                        from_zip: str = None):

        operation = Operations(optimizer_type, environment)

        operation.change_active_project()
        operation.create_scenario(creating_scenario_data)
        operation.upload_valid_input_files(not_download_list=not_download_input_list,
                                           folder=valid_input_files_folder,
                                           from_zip=from_zip)
        operation.save_defoult_scenario_pfr(True)
        operation.calculate_scenario()
        scenario_data = operation.get_scenario()

        if scenario_data.get('calculation_status') == 'success':

            kpi_data = operation.get_kpi_data()
            print(kpi_data)
            preview_output_tables = operation.get_preview_defoult_output_tables()
            print(preview_output_tables)

        else:
            print(scenario_data.get('calculation_message'))


if __name__ == "__main__":
    environment = 'LOCAL_STAGE'  # DEV LOCAL_STAGE DEMO_STAGE PROD
    optimizer_type = ProjectType.PROMO
    # scenario_id = 478

    # test = Test(optimizer_type, environment)
    # Test.input_validation(optimizer_type, environment)
    # Test.input_validation_all_optimizer(environment)

    # Test.check_validation_rules(optimizer_type)
    # Test.check_all_validation_rules()

    creating_scenario_data = None
    not_download_list = ['up_down_size']
    folder = 'calculation_success'
    Test.fill_new_scenario_and_calculate(optimizer_type, environment, creating_scenario_data, not_download_list, folder)

    # creating_scenario_data = None
    # zip_name = 'downloaded_inputs_9m'
    # Test.fill_new_scenario_and_calculate(optimizer_type, environment, creating_scenario_data, from_zip=zip_name)

    # _zip = 'C:/Users/LexSh/Downloads/test/25_Detailed_20240617_mb_Copy_1_20240626-10_39'
    # Test.create_scenario_and_filling_downloaded_data(optimizer_type, environment, _zip)
