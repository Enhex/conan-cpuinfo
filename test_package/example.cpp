#include <iostream>
#include <cpuinfo.h>

int main()
{
	cpuinfo_initialize();
	const auto l1_size = cpuinfo_get_processor(0)->cache.l1d->size;

	std::cout << "L1 Cache size: " << l1_size << std::endl;
}
