import os
import torch
from torch import nn
from torch.utils import model_zoo
from torchvision.models.resnet import BasicBlock, model_urls, Bottleneck
import torch.nn.functional as F
import numpy as np
import torchvision.models as models
#from vit_pytorch import ViT
#import vit_
from pytorch_pretrained_vit import ViT

class ResNet(nn.Module):
    def __init__(self, block, layers):
        self.inplanes = 64
        super(ResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
                               bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def improvement(self, rep):
        
        ###print("shape of reppp:", rep.shape)
        v = ViT('B_16_imagenet1k',
        pretrained = True,
        patches = 2,
        image_size = 28,
        num_classes = 2048,
        in_channels = 512,
        ).to("cuda")


        #print("shape of rep befor",rep_a[0].shape,"sssss",rep_a.view(1,1,32,2048).shape)
        #temp = torch.randn(64, 2048).to("cuda")
        #temp = v(rep)
        #print("shape of tempppp", temp.shape)
        #print("shapeeeeeeeee", temp.shape)

        '''temp_ = torch.empty_like(rep_b).to("cuda")
        for i in range(32):
            #print("shape of temp",temp.shape,"shape of view", v(rep_a[i].view(1,1,16,128)).shape)
            temp_[i] = v(rep_b[i].view(1,1,16,128))[0]'''

        #preds_a = v(rep_a.view(1,1,32,2048)) # (1, 1000)
        #print("shape of rep after",preds_a.shape)
        #preds_b = v(rep_b.view(1,1,32,2048))
        #return preds_a, preds_b
        return v(rep)

    
    
    
    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x, **kwargs):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        print("shapeeee",x.shape)
        x = self.layer2(x)
        #print("shapeeee",x.shape)
        #x = self.layer3(x)
        #x = self.layer4(x)

        #x = self.avgpool(x)
        #x = x.view(x.size(0), -1)
        #print("line 59999999",x.shape)
        x = self.improvement(x)
        #print("shape of xxxxxxx:", x.shape)

        return x


def resnet18(pretrained=True, **kwargs):
    model = ResNet(BasicBlock, [2, 2, 2, 2], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet18']), strict=False)
    return model


def resnet34(pretrained=True, **kwargs):
    model = ResNet(BasicBlock, [3, 4, 6, 3], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet34']))
    return model


def resnet50(pretrained=True, **kwargs):
    model = ResNet(Bottleneck, [3, 4, 6, 3], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet50']), strict=False)
    return model


def resnet101(pretrained=True, **kwargs):
    model = ResNet(Bottleneck, [3, 4, 23, 3], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet101']))
    return model


def resnet152(pretrained=True, **kwargs):
    model = ResNet(Bottleneck, [3, 8, 36, 3], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet152']))
    return model



class Convolution(nn.Module):
    def __init__(self, c_in, c_out):
        super(Convolution, self).__init__()
        self.conv = nn.Conv2d(c_in, c_out, 3, stride=1, padding=1)
        self.relu = nn.ReLU(True)

    def forward(self, x):
        return self.relu(self.conv(x))



class ConvNet(nn.Module):
    def __init__(self, c_hidden=64):
        super(ConvNet,self).__init__()
        self.conv1 = Convolution(3, c_hidden)
        self.conv2 = Convolution(c_hidden, c_hidden)
        self.conv3 = Convolution(c_hidden, c_hidden)
        self.conv4 = Convolution(c_hidden, c_hidden)

    def forward(self, x):
        # self._check_input(x)
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)
        x = self.conv2(x)
        x = F.max_pool2d(x, 2)
        x = self.conv3(x)
        x = F.max_pool2d(x, 2)
        x = self.conv4(x)
        x = F.max_pool2d(x, 2)
        return x.view(x.size(0), -1)