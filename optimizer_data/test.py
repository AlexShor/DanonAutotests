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
    def create_scenario_and_filling_full_data(optimizer_type: str, environment: str):

        operation = Operations(optimizer_type, environment)

        operation.change_active_project()
        operation.create_scenario()
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


if __name__ == "__main__":
    environment = 'PROD'  # DEV LOCAL_STAGE DEMO_STAGE PROD
    optimizer_type = ProjectType.CFR
    # scenario_id = 478

    # test = Test(optimizer_type, environment)
    # Test.input_validation(optimizer_type, environment)
    # Test.input_validation_all_optimizer(environment)

    # Test.check_validation_rules(optimizer_type)
    # Test.check_all_validation_rules()

    # Test.create_scenario_and_filling_full_data(optimizer_type, environment)

    _zip = 'C:/Users/LexSh/Downloads/test/25_Detailed_20240617_mb_Copy_1_20240626-10_39'
    scenario_data = {'cfr_group_id': 1, 'cfr_type_id': 1, 'cfr_randomizer_regime_id': 1}
    Test.create_scenario_and_filling_downloaded_data(optimizer_type, environment, _zip, scenario_data)
