import numpy as np
import torch
from torch.distributions import Normal, Independent

def generate_latent_future(dpn, first_ls_vector, seconds, default_frame_skip = 10, interpolate = False, clip = True, is_log_sigma = False):
    '''
    Use this function to generate the predicted the future latent vectors from a trained policy network.

    Assumes output of the network is the actual next frame, and not the epsilon perturbation.

    Parameters:
    ---------------
        dpn: Trained policy network (if you trained an Agent class, this would be the Agent.actor object).

        first_ls_vector: The first latent space vector to predict into the future. Must be a torch.Tensor object.

        seconds: Number of seconds to predict in to the future.

        default_frame_skip: During training it's useful to skip some number of frames. We will utilize linear interpolation to get the vectors between the predicted next-step vector.

        interpolate: When true will automatically do the interpolation filling in the missing frames.

        clip: Due to the non-normal distribution of our embedding, there are three elements of a LS vector that is always 0. During policy prediciton, these elements tend to naturally drift (potentially causing frame tearing). This clips those elements to 0.

        is_log_sigma: Some DPN output sigma always positive (either through an ELU activation) or premptively exponentiating the log output.

    Returns:
    ---------
        A numpy array containing enough latent space vectors to decode and create a 30fps video of number of seconds long.
    '''
    if interpolate:
        interpolate = lambda f, s: [(1-y)*f + y*s for y in np.linspace(0,1, default_frame_skip)]
    else:
        interpolate = lambda f,s:[f,s]
    if is_log_sigma:
        def get_mu_sigma(frame):
            mu, sigma = dpn(frame)
            sigma = torch.exp(sigma)
            return mu, sigma
    else:
        get_mu_sigma = lambda frame: dpn(frame)

    #calculate how many frames we need to build.
    number_of_passes = round((30/default_frame_skip)*seconds, 0)
    number_of_passes = int(number_of_passes)
    #initialize the current frame
    current = first_ls_vector.detach()
    output = []
    for i in  range(number_of_passes):
        mu, sigma = get_mu_sigma(first_ls_vector)
        dist = Independent(Normal(mu, sigma),1)
        next = dist.sample()
        if clip:
            x = next.numpy()
            x[16] = 0
            x[5] = 0
            x[9] = 0
            next = torch.as_tensor(x)
        interpolated = interpolate(current, next)
        output.extend(interpolated)
        current = next.detach()
    output = torch.tensor(output)
    return(output)
