"""Implements support vector machine."""

from __future__ import print_function
from __future__ import absolute_import

import numpy as np
from models.linear_model import LinearModel


class SupportVectorMachine(LinearModel):
    """Implements a linear regression mode model"""

    def backward(self, f, y):
        """Performs the backward operation based on the loss in total_loss.

        By backward operation, it means to compute the gradient of the loss
        w.r.t w.

        Hint: You may need to use self.x, and you made need to change the
        forward operation.

        Args:
            f(numpy.ndarray): Output of forward operation, dimension (N,1).
            y(numpy.ndarray): Ground truth label, dimension (N,1).
        Returns:
            total_grad(numpy.ndarray): Gradient of L w.r.t to self.w,
              dimension (ndims+1,).
        """
        reg_grad = self.w_decay_factor*self.w
        loss_grad = np.zeros((len(self.x[0]), 1))
        output = np.transpose(f) * y

        for i in range(len(output[0])):

            # This training example did have an error
            if(output[0, i] < 1):
                loss_grad[:, 0] = loss_grad[:, 0] - 1*self.x[i, :]*y[i]

        total_grad = reg_grad + loss_grad
        return total_grad

    def total_loss(self, f, y):
        """The sum of the loss across batch examples + L2 regularization.
        Total loss is hinge_loss + w_decay_factor/2*||w||^2

        Args:
            f(numpy.ndarray): Output of forward operation, dimension (N,1).
            y(numpy.ndarray): Ground truth label, dimension (N,1).
        Returns:
            total_loss (float): sum hinge loss + reguarlization.
        """
        # Implementation here.
        hinge_loss = np.sum(np.maximum(0, 1-np.transpose(f) * y))
        l2_loss = (self.w_decay_factor/2)*np.dot(np.transpose(self.w), self.w)
        total_loss = hinge_loss + l2_loss[0, 0]
        return total_loss

    def predict(self, f):
        """Converts score to prediction.

        Args:
            f(numpy.ndarray): Output of forward operation, dimension (N,1).
        Returns:
            (numpy.ndarray): Hard predictions from the score, f,
              dimension (N,1). Tie break 0 to 1.0.
        """
        for i in range(len(f)):
            if(f[i] >= 0):
                f[i] = 1
            else:
                f[i] = -1
        return f
