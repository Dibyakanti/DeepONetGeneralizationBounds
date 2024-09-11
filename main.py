import jax.numpy as jnp
from jax import random, vmap

from jax import config
# from jax.numpy import index_exp as index
# from jax.experimental.ode import odeint

# from tqdm import trange
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import maths
# from scipy.interpolate import griddata
# from scipy.integrate import dblquad

from scripts.data_generation import *
from scripts.DeepONet import *
from scripts.utils import *


if __name__=="__main__":
    # Define hyperparameters and grid:
    kappa = 1
    T_lim = 1 # corresponds to T

    #Size of rectangle
    x0 = 1
    y0 = 1


    # Initial condition
    num_fourier_terms = 2  # Number of sine terms in the Fourier series
    sine_amplitude = 0.2  # Amplitude of the sine terms

    # Training data
    m = 100   # grid size in each dimention for discretizing the inhomogenuoes term, which mean that m is the branch net input dimention and it has to be a perfect square
    N_train = 2**9  # number of inhomogenuoes term candidates ( i.e f)
    P_train = 4**6 # number of evaluation points for each training loss


    #----------------------------------TESTING-------------------------------

    # Test data
    N_test = 2**7 # number of test functions
    P_test = 3**6 # number of test collocation points

    'Data Generation'
    # Train

    key = random.PRNGKey(11)
    keys = random.split(key, N_train) # N keys to create N Functions

    config.update("jax_enable_x64", True)
    f_train, z_train, u_train = vmap(generate_one_training_data, (0, None, None, None, None, None, None))(keys, P_train, x0, y0, T_lim, m, sine_amplitude)

    #Reshape Data
    f_train = jnp.float32(f_train.reshape(N_train * P_train,-1))
    z_train = jnp.float32(z_train.reshape(N_train * P_train,-1))
    u_train = jnp.float32(u_train.reshape(N_train * P_train,-1))
    config.update("jax_enable_x64", False)

    # Test
    key = random.PRNGKey(4568) # different key than training data
    keys = random.split(key, N_test)

    config.update("jax_enable_x64", True)
    f_test1, z_test1, u_test1 = vmap(generate_one_test_data, (0, None, None, None, None, None, None))(keys, P_test, x0, y0, T_lim, m, sine_amplitude)

    #Reshape Data
    f_test = jnp.float32(f_test1.reshape(N_test * P_test,-1))
    z_test = jnp.float32(z_test1.reshape(N_test * P_test,-1))
    u_test = jnp.float32(u_test1.reshape(N_test * P_test,-1))

    config.update("jax_enable_x64", False)

    # Initialize model
    branch_layers = [m, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128]
    trunk_layers =  [3, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128]
    model = DeepONet(branch_layers, trunk_layers, loss_type= "l2", huber_delta=0.5**9)

    # Create dataset
    batch_size = 2**15
    don_dataset = DataGenerator(f_train, z_train, u_train, batch_size)
    test_dataset = [f_test, z_test, u_test]

    # Train
    model.train(don_dataset, test_dataset, nIter=10)

    save_checkpoint(model, 'model_checkpoint.npz')

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

    plt.savefig("./outputs/train_test_error_plots.png", bbox_inches ="tight")