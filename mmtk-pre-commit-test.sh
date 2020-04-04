
set -x
RUSTC_FLAGS="--no-default-features"
export RUSTFLAGS=-Awarnings

# Cargo check

cargo +nightly check --features nogc
cargo +nightly check --features semispace

cargo +nightly check --features nogc,sanity
cargo +nightly check --features semispace,sanity

cargo +nightly check --manifest-path vmbindings/jikesrvm/Cargo.toml --target=i686-unknown-linux-gnu --features nogc $RUSTC_FLAGS
cargo +nightly check --manifest-path vmbindings/jikesrvm/Cargo.toml --target=i686-unknown-linux-gnu --features semispace $RUSTC_FLAGS

cargo +nightly check --manifest-path vmbindings/openjdk/Cargo.toml --features nogc $RUSTC_FLAGS
cargo +nightly check --manifest-path vmbindings/openjdk/Cargo.toml --features semispace $RUSTC_FLAGS

cargo +nightly check --manifest-path vmbindings/dummyvm/Cargo.toml --features nogc $RUSTC_FLAGS
cargo +nightly check --manifest-path vmbindings/dummyvm/Cargo.toml --features semispace $RUSTC_FLAGS


# run build.py

# JikesRVM: Run lusearch

# OpenjDK:L Run 
