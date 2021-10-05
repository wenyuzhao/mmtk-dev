#include <stdlib.h>
#include "jvmti.h"

void check_jvmti_error(jvmtiEnv *jvmti, jvmtiError err, char* msg) {
    if (err != JVMTI_ERROR_NONE) {
        printf("CHECK_JVMTI_ERROR: %s : %d\n", msg, err);
        exit(err);
    }
}
