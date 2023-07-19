from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def generate_cavern_size(typical_size, size_deviation):
    """
    Generate a random cavern size based on a typical size and a size deviation.

    The generated size is drawn from a log-normal distribution, where the mean and standard deviation of the
    log-transformed sizes are determined by the typical_size and size_deviation parameters.

    Parameters:
    typical_size: float
        The typical or most common cavern size. This parameter determines the location (mean in the log scale) of the log-normal distribution.
        This should be a positive number, and it can be as large as desired.

    size_deviation: float
        The variation or deviation in cavern size.
        A deviation of 0 means that all holes will be exactly typical_size.
        A deviation of typical_size will make 5% of holes larger than 3 * typical_size and 5% smaller than typical_size / 3.
        A deviation of typical_size * 5 will make 5% of holes larger than 20 * typical_size and 5% smaller than typical_size / 20.

    Returns:
    int
        The generated cavern size, rounded to the nearest integer.
    """
    mu = np.log(typical_size)
    sigma = np.log1p(size_deviation / typical_size)
    hole_size = np.random.lognormal(mu, sigma)
    return hole_size


# Sample the cavern_size function
typical_size = 10

hole_sizes = np.zeros((50,10000))
for i, size_variation in enumerate(np.linspace(0,50,50)):
    # Calculate the corresponding hole size
    for n in range(10000):
        hole_sizes[i, n] = generate_cavern_size(typical_size, size_variation)

# plot the 95th percentile of each distribution
outliers = np.percentile(hole_sizes, 95, axis=1)
ax = plt.plot(np.linspace(0,50,50), outliers/typical_size)
plt.xlabel('Size variation')
plt.ylabel('Median cavern size')
plt.show()
