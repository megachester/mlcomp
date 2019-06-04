from mlcomp.task.executors.catalyst.base import BaseCallback
import pickle
from mlcomp.db.models import ReportImg
from catalyst.dl.state import RunnerState
import numpy as np


class F1Callback(BaseCallback):
    def on_batch_end(self, state: RunnerState):
        if state.loader_name != 'valid':
            return

        data = self.data[state.loader_name]
        targets = state.input['targets'].detach().cpu().numpy()
        preds = state.output['logits'].detach().cpu().numpy()
        data['target'].append(targets)
        data['output'].append(preds)

    def on_epoch_end(self, state: RunnerState):
        targets = np.hstack(self.data['valid']['target'])
        outputs = np.hstack(self.data['valid']['output'])
        img = self.info.plot(targets, outputs.argmax(1))
        content = {'img': img}
        obj = ReportImg(group=self.info.name, epoch=state.epoch, task=self.task.id,
                        img=pickle.dumps(content),
                        project=self.dag.project,
                        dag=self.task.dag,
                        part=state.loader_name
                        )

        self.img_provider.add(obj)
        self.img_provider.remove_lower(self.task.id, self.info.name, state.epoch)

        super(self.__class__, self).on_epoch_end(state)
