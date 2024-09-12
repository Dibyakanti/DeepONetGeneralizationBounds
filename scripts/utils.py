import numpy as np
from jax.flatten_util import ravel_pytree
import matplotlib.pyplot as plt


def save_checkpoint(params, filename):
    # Flatten parameters
    flat_params, unravel_fn = ravel_pytree(params)

    # Save the flattened parameters and the metadata
    np.savez(filename, params=flat_params, unravel_fn=unravel_fn)

def load_checkpoint(filename):
    # Load the checkpoint file
    data = np.load(filename)
    
    # Extract flattened parameters and unravel function
    flat_params = data['params']
    unravel_fn = data['unravel_fn'].item()  # Convert back to function
   
    # Unflatten parameters to the original structure
    params = unravel_fn(flat_params)
    
    return params

# 3D plot function
def plot_3d(ax, X, Y, u):
    surf = ax.plot_surface(X, Y, u, cmap='plasma')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$u(x,y,t)$')

# Color plot function
def plot(ax, X, Y, u):
    pcm = ax.pcolor(X, Y, u, cmap='plasma')
    plt.colorbar(pcm, ax=ax)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

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

def plot_train_test_error(model, filename):
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

    plt.savefig(f"./outputs/{filename}.png", bbox_inches ="tight")

    return

def plot_actual_pred(XX, YY, U_test, U_pred, time_steps):
   # Create a new figure with two rows of subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Top row: 3D plots
    # Analytical Solution of the Heat Equation
    axs[0, 0] = fig.add_subplot(221, projection='3d')
    plot_3d(axs[0, 0], XX, YY, U_test[0,:,:])
    axs[0, 0].set_title(f"Analytical Solution of the Heat Equation at t = {time_steps[0]:.1f}", fontsize='large')

    # Predicted Solution using DeepONet
    axs[0, 1] = fig.add_subplot(222, projection='3d')
    plot_3d(axs[0, 1], XX, YY, U_pred[0,:,:])
    axs[0, 1].set_title(f"Predicted Solution using DeepONet at t ={time_steps[0]:.1f}", fontsize='large')

    # Bottom row: 2D color plots
    # Analytical Solution of the Heat Equation
    plot(axs[1, 0], XX, YY, U_test[0,:,:])
    axs[1, 0].set_title(f"Analytical Solution of the Heat Equation at t = {time_steps[0]:.1f}", fontsize='large')

    # Predicted Solution using DeepONet
    plot(axs[1, 1], XX, YY, U_pred[0,:,:])
    axs[1, 1].set_title(f"Predicted Solution using DeepONet at t = {time_steps[0]:.1f}", fontsize='large')

    plt.savefig("./outputs/actual_predicted_plots.png", bbox_inches ="tight")

    return