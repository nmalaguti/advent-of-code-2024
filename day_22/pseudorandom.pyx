# Cython speed directives
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: language_level=3
# cython: use_unlikely=False

cdef inline long long mix(long long a, long long b) noexcept nogil:
    return a ^ b

cdef inline long long prune(long long x) noexcept nogil:
    # Equivalent to x % 16777216, but faster using bitmask if positive
    # 16777216 == 2**24, so use & 0xFFFFFF
    return x & 0xFFFFFF

cpdef int pseudorandom(int secret, int steps=1) noexcept nogil:
    cdef long long s = <long long>secret
    cdef int i
    for i in range(steps):
        s = prune(mix(s, s << 6))
        s = prune(mix(s, s >> 5))
        s = prune(mix(s, s << 11))
    return <int>s
