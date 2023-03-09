#include <stdlib.h>
#include <cilk/cilk.h>


#define n 1024

double a[n][n];
double b[n][n];
double c[n][n];

int main()
{
	for (int i = 0; i < n; i++)
		for (int j = 0; j < n; j++)
		{
			a[i][j] = (double)rand() / 1000;
			b[i][j] = (double)rand() / 1000;
			c[i][j] = 0;
		}
	cilk_for (int i = 0; i < n; i++)
		for (int k = 0; k < n; k++)
			for (int j = 0; j < n; j++)
				c[i][j] += a[i][k]*b[k][j];

	return 0;
}
