import numpy as np
import jax.numpy as jnp
from jax.flatten_util import ravel_pytree
import matplotlib.pyplot as plt
import seaborn as sb
import matplotlib.ticker as ticker
from scipy.interpolate import griddata
import configparser

# 3D plot function
def plot_3d(ax, X, T, f):
    surf = ax.plot_surface(X, T, f, cmap='viridis')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$t$')
    ax.set_zlabel('$s(x,t)$')

# Color plot function
def plot(ax, X, T, f):
    pcm = ax.pcolor(X, T, f, cmap='viridis')
    plt.colorbar(pcm, ax=ax)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$t$')

# Error plot function
def plot_us(x,u,y,s):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.rcParams['font.size'] = '18'
    color='#440154'
    wdt=1.5
    ax1.plot(x,u,'k--',label='$u(x)=ds/dx$',linewidth=wdt)
    ax1.plot(y,s,'-',label='$s(x)=s(0)+\int u(t)dt|_{t=y}$',linewidth=wdt)
    ax1.set_xlabel('x')
    ax1.set_ylabel('u')
    ax1.tick_params(axis='y', color=color)
    ax1.legend(loc = 'lower right', ncol=1)

def plot_tr_dynamics(model, P_train):
    # Visualizations
    fig, axs = plt.subplots(1, 3, figsize=(24, 6))

    # Colors from the 'viridis' colormap
    medium_purple = '#5B278F'
    light_purple = '#3b528b'
    viri_green = '#00A896'

    # Total loss per 100 iteration
    total_loss_eval_numbers = range(1, len(model.loss_don_log) + 1)
    axs[0].plot(total_loss_eval_numbers, model.loss_don_log, '--', color=medium_purple, label='Training loss')
    axs[0].set_yscale('log')
    axs[0].set_xlabel(r'Iterations (Scaled by $10^2$)', fontsize='large')
    axs[0].set_ylabel('Training Loss', fontsize='large')
    axs[0].set_title('Evolution of Training Loss Over Iterations', fontsize='large')

    # Test loss
    test_loss_eval_numbers = range(1, len(model.loss_test_log) + 1)
    axs[1].plot(test_loss_eval_numbers, model.loss_test_log, '--', color=medium_purple, label='Test loss')
    axs[1].set_yscale('log')
    axs[1].set_xlabel(r'Iterations (Scaled by $10^2$)', fontsize='large')
    axs[1].set_ylabel('Test Loss', fontsize='large')
    axs[1].set_title('Evolution of Test Loss Over Iterations', fontsize='large')

    # Average fractional test loss
    AFTL_eval_numbers = range(1, len(model.loss_AF_test_log) + 1)
    axs[2].plot(AFTL_eval_numbers, model.loss_AF_test_log, '--', color=medium_purple, label='Average Fractional Test loss')
    axs[2].set_yscale('log')
    axs[2].set_xlabel(r'Iterations (Scaled by $10^2$)', fontsize='large')
    axs[2].set_ylabel('Average Fractional Test Loss', fontsize='large')
    axs[2].set_title('Evolution of Average Fractional Test Loss over Iterations', fontsize='large')

    plt.tight_layout()
    plt.savefig(f"plot_tr_dynamics_ptrain{P_train}_losstype{model.loss_type}.png")

    return