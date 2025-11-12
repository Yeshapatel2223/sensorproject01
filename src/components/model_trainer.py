import sys
from typing import Dict
import os
import numpy as np
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUnits
from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    trained_model_path: str = os.path.join(artifact_folder, 'model.pkl')
    expected_accuracy: float = 0.45
    model_config_file_path: str = os.path.join('config', 'model.yaml')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.utils = MainUnits()
        self.models = {
            'XGBClassifier': XGBClassifier(),
            'GradientBoostingClassifier': GradientBoostingClassifier(),
            'SVC': SVC(),
            'RandomForestClassifier': RandomForestClassifier()
        }

    def evaluate_models(self, x, y, models: Dict):
        """Train and evaluate models and return dict of model_name: accuracy"""
        try:
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            report = {}

            for name, model in models.items():
                model.fit(x_train, y_train)
                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                train_acc = accuracy_score(y_train, y_train_pred)
                test_acc = accuracy_score(y_test, y_test_pred)
                report[name] = test_acc

                logging.info(f"{name}: Train={train_acc:.3f}, Test={test_acc:.3f}")

            return report

        except Exception as e:
            raise CustomException(e, sys)

    def get_best_model(self, x_train, y_train, x_test, y_test):
        """Return best model, its name, and accuracy."""
        try:
            model_report = self.evaluate_models(
                np.concatenate((x_train, x_test)),
                np.concatenate((y_train, y_test)),
                self.models
            )

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model_object = self.models[best_model_name]

            return best_model_name, best_model_object, best_model_score

        except Exception as e:
            raise CustomException(e, sys)

    def finetune_best_model(self, best_model_object, best_model_name, x_train, y_train):
        """Fine-tune the best model using parameters from YAML config."""
        try:
            model_config = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)
            param_grid = model_config['model_selection']['model'][best_model_name]['search_param_grid']

            grid_search = GridSearchCV(best_model_object, param_grid=param_grid, cv=5, n_jobs=-1, verbose=1)
            grid_search.fit(x_train, y_train)

            best_params = grid_search.best_params_
            logging.info(f"Best Parameters for {best_model_name}: {best_params}")

            finetuned_model = best_model_object.set_params(**best_params)
            return finetuned_model

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self, train_array, test_array):
        """Main function to initiate model training, tuning, and saving."""
        try:
            logging.info("Splitting training and testing features and target variables")

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            logging.info("Evaluating models...")
            best_model_name, best_model, best_model_score = self.get_best_model(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test
            )

            logging.info(f"Best model found: {best_model_name} with accuracy {best_model_score:.3f}")

            # Fine-tune the best model
            best_model = self.finetune_best_model(
                best_model_object=best_model,
                best_model_name=best_model_name,
                x_train=x_train,
                y_train=y_train
            )

            # Re-train with fine-tuned model
            best_model.fit(x_train, y_train)
            y_pred = best_model.predict(x_test)
            final_accuracy = accuracy_score(y_test, y_pred)

            logging.info(f"Final {best_model_name} accuracy after fine-tuning: {final_accuracy:.3f}")

            if final_accuracy < self.model_trainer_config.expected_accuracy:
                raise CustomException("No model found with accuracy above expected threshold", sys)

            # Save the best model
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path), exist_ok=True)
            self.utils.save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=best_model
            )

            logging.info(f"Model saved successfully at: {self.model_trainer_config.trained_model_path}")
            return self.model_trainer_config.trained_model_path

        except Exception as e:
            raise CustomException(e, sys)
