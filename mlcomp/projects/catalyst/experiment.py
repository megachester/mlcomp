from collections import OrderedDict
import torchvision
import numpy as np
from torchvision import transforms
from catalyst.dl.experiments import ConfigExperiment


class Experiment(ConfigExperiment):
    @staticmethod
    def get_transforms(stage: str = None, mode: str = None):
        return transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]
        )

    def get_datasets(self, stage: str, **kwargs):
        datasets = OrderedDict()

        trainset = torchvision.datasets.CIFAR10(
            root='./data',
            train=True,
            download=True,
            transform=Experiment.get_transforms(stage=stage, mode="train")
        )
        testset = torchvision.datasets.CIFAR10(
            root='./data',
            train=False,
            download=True,
            transform=Experiment.get_transforms(stage=stage, mode="valid")
        )

        trainset.train_data = trainset.train_data[:32]
        trainset.train_labels = np.clip(trainset.train_labels[:32], 0, 1)

        testset.train_data = trainset.train_data[:32]
        testset.train_labels = np.clip(trainset.train_labels[:32], 0, 1)

        testset.test_data = testset.test_data[:32]
        testset.test_labels = np.clip(testset.test_labels[:32], 0, 1)

        datasets["train"] = trainset
        datasets["valid"] = testset

        return datasets