#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "jvmti.h"
#include "common.h"
#include <err.h>

static jvmtiCapabilities caps;
static jvmtiEventCallbacks callbacks;

#define DEBUG

static void JNICALL TOTAL_ALLOCATION_native_alloc(JNIEnv *env, jclass klass, jobject o) {
    //alloc(&o);
}

static void JNICALL VMObjectAlloc(jvmtiEnv *jvmti_env, JNIEnv* jni_env, jthread thread, jobject object, jclass object_klass, jlong size) {
    #ifdef DEBUG
    printf("alloc %p %lu\n", *(void**)object, size);
    #endif
}

static void JNICALL VMStart(jvmtiEnv *jvmti_env, JNIEnv* jni_env) {
    #ifdef DEBUG
    printf("VMStart\n");
    #endif
    jclass klass;
    jfieldID field;
    jint rc;

    static JNINativeMethod registry[1] = {
        {"alloc", "(Ljava/lang/Object;)V",
            (void*)&TOTAL_ALLOCATION_native_alloc}
    };

    /* Register Natives for class whose methods we use */
    klass = (*jni_env)->FindClass(jni_env, "TotalAllocation");
    if (klass == NULL) {
        err(1, "ERROR: JNI: Cannot find %s with FindClass\n", "TotalAllocation");
    }
    rc = (*jni_env)->RegisterNatives(jni_env, klass, registry, 1);
    if (rc != 0) {
        err(1, "ERROR: JNI: Cannot register natives for class %s\n", "TotalAllocation");
    }

    field = (*jni_env)->GetStaticFieldID(jni_env, klass, "enabled", "I");
    if (field == NULL) {
        err(1, "ERROR: JNI: Cannot get field from %s\n", "TotalAllocation");
    }
    (*jni_env)->SetStaticIntField(jni_env, klass, field, 1);
}

JNIEXPORT jint JNICALL Agent_OnLoad(JavaVM *jvm, char *options, void *reserved) {
    jvmtiEnv *jvmti;
    #ifdef DEBUG
    printf("JVMTI agent for counting total allocation size\n");
    #endif

    (*jvm)->GetEnv(jvm, (void**) &jvmti, JVMTI_VERSION_1_0);
    
    jvmtiError error;

    // Add capabilities
    memset(&caps, 0, sizeof(jvmtiCapabilities));
    caps.can_generate_vm_object_alloc_events = 1;
    error = (*jvmti)->AddCapabilities(jvmti, &caps);
    check_jvmti_error(jvmti, error, "Failed to add JVMTI capabilities");
    // Add callbacks
    memset(&callbacks, 0, sizeof(jvmtiEventCallbacks));
    callbacks.VMStart = &VMStart;
    callbacks.VMObjectAlloc = &VMObjectAlloc;
    error = (*jvmti)->SetEventCallbacks(jvmti, &callbacks, (jint) sizeof(callbacks));
    check_jvmti_error(jvmti, error, "Failed to add JVMTI callbacks");
    // Enable notifications
    error = (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_VM_START, (jthread)NULL);
    check_jvmti_error(jvmti, error, "Failed to set nofication for VMStart");
    error = (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_VM_OBJECT_ALLOC, (jthread)NULL);
    check_jvmti_error(jvmti, error, "Failed to set nofication for VMObjectAlloc");

    return JNI_OK;
}
