# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Contains the SageMaker Experiment class."""
from smexperiments import _base_types, api_types, trial, _utils, trial_component
import time


class Experiment(_base_types.Record):
    """
    An Amazon SageMaker experiment, which is a collection of related trials.
    New experiments are created by calling :meth:`~smexperiments.experiment.Experiment.create`. Existing
    experiments can be reloaded by calling :meth:`~smexperiments.experiment.Experiment.load`. You can
    add a new trial to an Experiment by calling :meth:`~smexperiments.experiment.Experiment.create_trial`.
    To remove an experiment and associated trials, trial components by calling :meth:`~smexperiments.experiment
    .Experiment.delete_all`.
    Examples:
        .. code-block:: python
            from smexperiments import experiment
            my_experiment = experiment.Experiment.create(experiment_name='AutoML')
            my_trial = my_experiment.create_trial(trial_name='random-forest')
            for exp in experiment.Experiment.list():
                print(exp)
            for trial in my_experiment.list_trials():
                print(trial)
            my_experiment.delete_all(action="--force")
    Attributes:
        experiment_name (str): The name of the experiment. The name must be unique within an account.
        description (str): A description of the experiment.
        tags (List[dict[str, str]]): A list of tags to associate with the experiment.
    """

    experiment_name = "tes-experiment-jose"
    description = "This is a test"
    tags = None

    _boto_create_method = "create_experiment"
    _boto_load_method = "describe_experiment"
    _boto_update_method = "update_experiment"
    _boto_delete_method = "delete_experiment"

    _boto_update_members = ["experiment_name", "description", "display_name"]
    _boto_delete_members = ["experiment_name"]

    MAX_DELETE_ALL_ATTEMPTS = 3

    def save(self):
        """Save the state of this Experiment to SageMaker.
        Returns:
            dict: Update experiment API response.
        """
        return self._invoke_api(self._boto_update_method, self._boto_update_members)

    def delete(self):
        """Delete this Experiment from SageMaker.
        Deleting an Experiment requires that each Trial in the Experiment is first deleted.
        Returns:
            dict: Delete experiment API response.
        """
        return self._invoke_api(self._boto_delete_method, self._boto_delete_members)

    @classmethod
    def load(cls, experiment_name, sagemaker_boto_client=None):
        """
        Load an existing experiment and return an ``Experiment`` object representing it.
        Args:
            experiment_name: (str): Name of the experiment
            sagemaker_boto_client (SageMaker.Client, optional): Boto3 client for SageMaker.
                If not supplied, a default boto3 client will be created and used.
        Returns:
            sagemaker.experiments.experiment.Experiment: A SageMaker ``Experiment`` object
        """
        return cls._construct(
            cls._boto_load_method,
            experiment_name=experiment_name,
            sagemaker_boto_client=sagemaker_boto_client,
        )

    @classmethod
    def create(cls, experiment_name=none, description=none, tags=None, sagemaker_boto_client=None):
        """
        Create a new experiment in SageMaker and return an ``Experiment`` object.
        Args:
            experiment_name: (str): Name of the experiment. Must be unique. Required.
            experiment_description: (str, optional): Description of the experiment
            sagemaker_boto_client (SageMaker.Client, optional): Boto3 client for SageMaker. If not
                supplied, a default boto3 client will be created and used.
            tags (List[dict[str, str]]): A list of tags to associate with the experiment.
        Returns:
            sagemaker.experiments.experiment.Experiment: A SageMaker ``Experiment`` object
        """
        return cls._construct(
            cls._boto_create_method,
            experiment_name=experiment_name,
            description=description,
            tags=tags,
            sagemaker_boto_client=sagemaker_boto_client,
        )

    

 
