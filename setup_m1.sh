#!/bin/bash
# 
# M1 Max Setup Script for CreativeGAN-Rhythm
# Optimized for Apple Silicon machines running macOS Sequoia
#

set -e

echo "🚀 Setting up CreativeGAN-Rhythm for M1 Max..."
echo

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is optimized for macOS. For other systems, use:"
    echo "   pip install -r requirements.txt"
    echo
    exit 1
fi

# Check if running on Apple Silicon
ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    echo "⚠️  This script is optimized for Apple Silicon (M1/M2). Detected: $ARCH"
    echo "   For Intel Macs, use: pip install -r requirements.txt"
    echo
    exit 1
fi

echo "✅ Detected Apple Silicon ($ARCH) on macOS"
echo

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "🐍 Python version: $PYTHON_VERSION"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "✅ Python version is compatible"
else
    echo "❌ Python 3.9+ required. Please upgrade Python."
    exit 1
fi
echo

# Install Homebrew dependencies
echo "🍺 Installing Homebrew dependencies..."
if command -v brew >/dev/null 2>&1; then
    echo "✅ Homebrew is installed"
else
    echo "❌ Homebrew not found. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "📦 Installing FluidSynth for audio synthesis..."
brew install fluidsynth || echo "⚠️  FluidSynth installation warning (may already be installed)"
echo

# Install Python dependencies
echo "📦 Installing Python dependencies optimized for M1 Max..."
if pip3 install -r requirements-m1.txt; then
    echo "✅ M1 Max dependencies installed successfully"
else
    echo "❌ Failed to install M1 dependencies. Trying fallback..."
    pip3 install -r requirements.txt
fi
echo

# Test the installation
echo "🧪 Testing installation..."
python3 -c "
import sys
sys.path.append('./rhythm_can')
from rhythm_can.m1_optimization import configure_tensorflow_for_m1, print_system_info, get_optimized_imports

print('🔍 System Information:')
print_system_info()
print()

print('⚙️  Testing TensorFlow configuration...')
try:
    tf = configure_tensorflow_for_m1()
    imports = get_optimized_imports()
    print('✅ TensorFlow configuration successful')
    print(f'✅ Loaded {len(imports)} optimized imports')
    print()
    
    # Test basic model creation
    Input, Dense, Model = imports['Input'], imports['Dense'], imports['Model']
    test_model = Model(inputs=Input(shape=(100,)), outputs=Dense(32)(Input(shape=(100,))))
    print('✅ Model creation test passed')
    
    print('🎉 Installation successful!')
    print()
    print('📝 Next steps:')
    print('   1. Open: jupyter notebook M1_Max_Optimization_Guide.ipynb')
    print('   2. Run any of the optimized notebooks (*-gm.ipynb)')
    print('   3. Start training your Creative GAN models!')
    
except Exception as e:
    print(f'❌ Installation test failed: {e}')
    print('Please check the error messages above and try again.')
    sys.exit(1)
"

echo
echo "🎵 CreativeGAN-Rhythm is ready for M1 Max training!"
echo "📖 Read M1_MAX_README.md for detailed usage instructions"
echo