#include <stdlib.h>


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
	for (int ib = 0; ib < n; ib += 32)
		for (int kb = 0; kb < n; kb += 32)
			for (int jb = 0; jb < n; jb += 32)
				for (int i = 0; i < 32; i++)
					for (int k = 0; k < 32; k++)
						for (int j = 0; j < 32; j++)
							c[ib + i][jb + j] += a[ib + i][kb + k]*b[kb + k][jb + j];
	return 0;
}
