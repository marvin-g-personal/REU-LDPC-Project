import torch
import torch.nn.functional as F
from torch_geometric.nn import GPSConv
from torch_geometric.data import Data

import tensorflow as tf
from tensorflow.keras.layers import Layer
import numpy as np

from decoder import * 

## Generative Adversarial Network approach

# Should  use specifically 5G standard LDPC/Polar codes
    # Main algorithms for,
        # LDPC: Belief Propagation
        # Polar: Successive Cancellation Listing, Successive Cancellation

    # Could store different weights for generator and discriminator, 
    # make a super noise generator that will always attack really good at the discriminator 
class DataSet():
    def __init__(self):
        pass
    

# Construct generator (encoder using forward diffusion to simulate channel)
    # By simulating channel it will try to come up with ways to fool discriminator/decoder
    # through noising the original codeword

    # Could make a general generator for GNN, ECCT, DDECCT, and AECC(Adversarial Error Correcting Code) 
    # to compare how different models learn or have weaknesses in decoding. 
class Generator(Layer):
    def __init__(self):
        pass

    def call(self, c):
        emb = 
        return z

    def create_mask(self, H):
        return H_mask
        

# Construct discriminator (decoder using reverse diffusion)
    # Will have to come up with ways to try to decode the noised codeword against specific noise
    # that will be trying to fool it. 
    
    # For optimization:
        # use Linformer having a O(n) on top of already improved complexity using the pcm mask
        # use split diffusion to improve accuracy and efficiency by guiding model rather than EMA

class Discriminator(Layer):
    def __init__(self, ls_active=True):
        self.beta 
        self.betas_bar
        self.ls_active = ls_active

        self.src_embed
        self.time_embed
        self.fc
        
    def call(self, r_t):
        for i in range(self.pcm.shape[0]):
            r_t, z_hat, t = self.rev_diff_call(r_t)
            
            if (r_t @ self.pcm)==0:
                return r_t, z_hat, i            
        return r_t, z_hat, i

    # Refines recieved codeword r at time t
    def rev_diff_call(self, r_t): 
        t = ( self.pcm @ to_bin(r_t) ).sum() # ix for the 'time step' t in the diffusion # 'time step' t is really a error estimate of the syndrome
        z_hat = self.tran_call(r_t, t)
        
        factor = ( self.betas_bar[t]*self.beta[t] / (self.betas_bar[t] + self.beta[t]) ) # theoretical step size
        err_hat = r_t - tf.sign(z_hat*rt)
        l = self.line_search() if self.ls_active else 1.

        r_t1 = r_t - (l * factor * err_hat) # refined estimate of the codeword for the diffusion step
        # r_t1[t==0] = r_t[t==0] # if cw has 0 synd. keep as is
        return r_t1, z_hat, t # r at time t-1

    # optimal lambda l for theoretical and for error prediction
    def line_search(self, factor, err_hat):
        l_values = tf.linespace(1., 20., 20).reshape(1,1,20)
        syndromes = to_bin(r_t - l_values*(factor*err_hat)) @ self.pcm
        ix = syndromes.argmin() # get the index of the min syndrome
        return l_values[ix]
        
    # Extracts noise estimate z_hat from r
    def tran_call(self, r_t, t):
        syndrome = self.pcm @ to_bin(r_t) #(m,1) check nodes
        magnitude = tf.abs(r_t) #(n,1) variable nodes

        nodes = tf.concat([magnitude, syndrome]) # data for vertices, shape (n+m,1)
        
        emb = self.src_emb * nodes
        time_emb = self.time_embed(t) 
        
        emb_t = time_emb * emb
        emb_t = self.decoder(emb_t, self.mask, time_emb)
        z_hat = self.fc(emb_t)
        return z_hat


class E2EModel(tf.keras.Model):
    def __init__(self):
        pass















        
