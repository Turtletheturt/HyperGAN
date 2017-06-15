import tensorflow as tf
import hyperchamber as hc
import os
import hypergan
from hypergan.discriminators.common import *

from hypergan.discriminators.pyramid_discriminator import PyramidDiscriminator
from hypergan.generators.resize_conv_generator import ResizeConvGenerator
from .base_discriminator import BaseDiscriminator

class AutoencoderDiscriminator(BaseDiscriminator):

    def build(self, net):
        config = self.config
        gan = self.gan
        ops = self.ops

        print("GAN", gan.config)
        generator = config.decoder(gan, gan.generator.config)
        generator.ops = ops # share variable allocation to make variables part of the discriminator training step

        encoder = config.encoder(gan, config)
        encoder.ops = ops
        ops.describe("autoencoder-d")
        hidden = encoder.build(net)
        ops.describe("autoencoder-g")
        reconstruction = generator.build(hidden)
        print("[autoencoder discriminator] hidden layer ", hidden)

        error = config.distance(net, reconstruction)

        self.reconstruction = reconstruction

        return error


