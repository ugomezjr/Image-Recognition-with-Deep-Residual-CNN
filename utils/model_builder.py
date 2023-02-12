import torch
from torch import nn

def conv_block(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]  # inplace=True - modifies the input tensor directly without the allocation of additional memory.
    if pool: layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)


class ResidualBlock(nn.Module):
    def __init__(self, hidden_shape, stride=1):
        super().__init__()

        self.conv_block = nn.Sequential(
            conv_block(hidden_shape, hidden_shape),                            
            conv_block(hidden_shape, hidden_shape)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv_block(x) + x


class ResNet_18_Layer(nn.Module):
    """Creates the 18-layer ResNet architecture.

  Replicates the 18-layer ResNet architecture from the 
  paper Deep Residual Learning for Image Recognition in PyTorch.

  See the paper here: https://arxiv.org/abs/1512.03385

  Args:
    input_shape: An integer indicating number of input channels.
    hidden_units: An integer indicating number of hidden units between layers.
    output_shape: An integer indicating number of output units.
  """
    def __init__(self) -> None:
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=7, stride=2, padding=3)
        
        self.conv2_x = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            ResidualBlock(hidden_shape=64),
            ResidualBlock(hidden_shape=64))
        
        self.conv3_1 = conv_block(in_channels=64, out_channels=128, pool=True)
        
        self.conv3_x = nn.Sequential(
            ResidualBlock(hidden_shape=128),
            ResidualBlock(hidden_shape=128))
        
        self.conv4_1 = conv_block(in_channels=128, out_channels=256, pool=True)
        
        self.conv4_x = nn.Sequential(
            ResidualBlock(hidden_shape=256),
            ResidualBlock(hidden_shape=256))
        
        self.conv5_1 = conv_block(in_channels=256, out_channels=512, pool=True)
        
        self.conv5_x = nn.Sequential(
            ResidualBlock(hidden_shape=512),
            ResidualBlock(hidden_shape=512))

        self.classifier = None


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.conv2_x(x)
        x = self.conv3_x( self.conv3_1(x) )
        x = self.conv4_x( self.conv4_1(x) )
        return self.conv5_x( self.conv5_1(x) )