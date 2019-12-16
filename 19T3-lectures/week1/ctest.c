#include <stdio.h>
#include <assert.h>

double sum(double a, double b) {
    return a + b;
}

int main() {
    assert(sum(1, 2) == 3);
    assert(sum(2, 2) == 4);
    assert(sum(3, 2) == 5);
    printf("All tests passed\n");
}