"""
M1 Max optimization utilities for CreativeGAN-Rhythm
Optimized for Apple Silicon with TensorFlow 2.x and Metal GPU support
"""

import os
import warnings
import platform

def check_m1_compatibility():
    """Check if running on compatible M1 Max system"""
    machine = platform.machine()
    system = platform.system()
    
    if system == 'Darwin' and machine == 'arm64':
        print("✅ Running on Apple Silicon (M1/M2)")
        return True
    else:
        print(f"ℹ️  Running on {system} {machine} - using CPU/standard GPU optimizations")
        return False

def configure_tensorflow_for_m1():
    """Configure TensorFlow for optimal performance on M1 Max"""
    try:
        import tensorflow as tf
    except ImportError:
        print("❌ TensorFlow not installed. Please install with:")
        if check_m1_compatibility():
            print("   pip install tensorflow-macos tensorflow-metal")
        else:
            print("   pip install tensorflow")
        raise
    
    print(f"✅ TensorFlow {tf.__version__} loaded")
    
    # Configure GPU if available
    try:
        # Try to configure GPU (Metal on M1, CUDA on others)
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"✅ Configured {len(gpus)} GPU(s) with memory growth enabled")
        else:
            print("ℹ️  No GPU detected, using CPU")
    except Exception as e:
        print(f"⚠️  GPU configuration warning: {e}")
    
    # Configure for optimal performance
    try:
        # Set thread configuration
        tf.config.threading.set_intra_op_parallelism_threads(0)  # Use all available cores
        tf.config.threading.set_inter_op_parallelism_threads(0)  # Use all available cores
        
        # Enable mixed precision training if supported
        if tf.__version__.startswith('2.'):
            try:
                policy = tf.keras.mixed_precision.Policy('mixed_float16')
                tf.keras.mixed_precision.set_global_policy(policy)
                print("✅ Mixed precision training enabled")
            except Exception as e:
                print(f"ℹ️  Mixed precision not enabled: {e}")
        
    except Exception as e:
        print(f"⚠️  Performance configuration warning: {e}")
    
    print(f"✅ TensorFlow configured for {platform.machine()} architecture")
    
    return tf

def get_optimized_imports():
    """Get TensorFlow 2.x compatible imports"""
    try:
        import tensorflow as tf
    except ImportError:
        print("❌ TensorFlow not installed")
        return {}
    
    # Check TensorFlow version
    tf_version = tf.__version__
    if tf_version.startswith('1.'):
        print(f"⚠️  TensorFlow {tf_version} detected. Please upgrade to 2.x for M1 optimization")
        print("   pip install --upgrade tensorflow")
    
    # Modern TF 2.x imports
    imports = {
        'tf': tf,
        'keras': tf.keras,
        'Input': tf.keras.layers.Input,
        'Dense': tf.keras.layers.Dense,
        'Flatten': tf.keras.layers.Flatten,
        'Dropout': tf.keras.layers.Dropout,
        'Reshape': tf.keras.layers.Reshape,
        'LSTM': tf.keras.layers.LSTM,
        'Bidirectional': tf.keras.layers.Bidirectional,
        'Embedding': tf.keras.layers.Embedding,
        'Concatenate': tf.keras.layers.Concatenate,
        'Conv2D': tf.keras.layers.Conv2D,
        'Conv2DTranspose': tf.keras.layers.Conv2DTranspose,
        'BatchNormalization': tf.keras.layers.BatchNormalization,
        'LeakyReLU': tf.keras.layers.LeakyReLU,
        'RMSprop': tf.keras.optimizers.RMSprop,
        'Adam': tf.keras.optimizers.Adam,
        'Model': tf.keras.Model,
        'Sequential': tf.keras.Sequential,
        'Lambda': tf.keras.layers.Lambda,
        'Softmax': tf.keras.layers.Softmax,
        'UpSampling2D': tf.keras.layers.UpSampling2D,
        'Activation': tf.keras.layers.Activation,
        'RepeatVector': tf.keras.layers.RepeatVector,
        'multiply': tf.keras.layers.multiply,
        'regularizers': tf.keras.regularizers,
        'EarlyStopping': tf.keras.callbacks.EarlyStopping,
        'ModelCheckpoint': tf.keras.callbacks.ModelCheckpoint,
        'TensorBoard': tf.keras.callbacks.TensorBoard,
        'to_categorical': tf.keras.utils.to_categorical,
        'K': tf.keras.backend
    }
    
    print(f"✅ Loaded {len(imports)} optimized imports")
    return imports

def set_environment_variables():
    """Set optimized environment variables"""
    # Remove CUDA-specific variables that might interfere
    cuda_vars = ['CUDA_VISIBLE_DEVICES', 'CUDA_DEVICE_ORDER']
    removed_vars = []
    for var in cuda_vars:
        if var in os.environ:
            del os.environ[var]
            removed_vars.append(var)
    
    if removed_vars:
        print(f"✅ Removed CUDA variables: {', '.join(removed_vars)}")
    
    # Set optimizations based on platform
    if check_m1_compatibility():
        # M1-specific optimizations
        os.environ['TF_METAL_DEVICE_VERBOSE'] = '1'  # Enable Metal GPU verbose logging
    
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'     # Reduce TensorFlow logging
    print("✅ Environment variables configured")

def print_system_info():
    """Print system information for debugging"""
    print("🖥️  System Information:")
    print(f"   Platform: {platform.platform()}")
    print(f"   Machine: {platform.machine()}")
    print(f"   Processor: {platform.processor()}")
    print(f"   Python: {platform.python_version()}")
    
    try:
        import tensorflow as tf
        print(f"   TensorFlow: {tf.__version__}")
        
        # List available devices
        devices = tf.config.list_physical_devices()
        print(f"   Devices: {len(devices)}")
        for device in devices:
            print(f"     - {device}")
            
    except ImportError:
        print("   TensorFlow: Not installed")

# Auto-configure when imported (can be disabled by setting environment variable)
if __name__ != "__main__" and os.environ.get('SKIP_AUTO_CONFIG') != '1':
    set_environment_variables()
    
    # Only configure TensorFlow if it's available
    try:
        tf = configure_tensorflow_for_m1()
    except ImportError:
        print("ℹ️  TensorFlow not available, skipping auto-configuration")
        tf = None