// Exact degree-six erasure at stable budget 20 with five added pairs.
#define AC_ROUND08_MAGNUS_NATIVE_LIBRARY
#include "round07_magnus_native.cpp"

int main() {
    magnus_native::run<6, 7>(10, false, true);
}
