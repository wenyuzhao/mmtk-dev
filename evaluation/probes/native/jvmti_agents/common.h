#include "jvmti.h"
#ifndef COMMON_H_
#define COMMON_H_
void check_jvmti_error(jvmtiEnv *jvmti, jvmtiError err, char* msg);
#endif
