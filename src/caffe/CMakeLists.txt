# generate protobuf sources
file(GLOB proto_files proto/*.proto)
caffe_protobuf_generate_cpp_py(${proto_gen_folder} proto_srcs proto_hdrs proto_python ${proto_files})

# include python files either to force generation
add_library(proto STATIC ${proto_hdrs} ${proto_srcs} ${proto_python})
caffe_default_properties(proto)
target_link_libraries(proto PUBLIC ${PROTOBUF_LIBRARIES})
#target_include_directories(proto PUBLIC ${PROTOBUF_INCLUDE_DIR})

#list(INSERT Caffe_LINKER_LIBS 0 PUBLIC proto) # note, crucial to prepend!

# --[ Caffe library

# creates 'test_srcs', 'srcs', 'test_cuda', 'cuda' lists
caffe_pickup_caffe_sources(${PROJECT_SOURCE_DIR})

# add this option here since CUDA will not honor
# target_compile_definitions

add_library(caffe ${srcs})

if(WIN32)
  target_link_libraries(caffe ${Caffe_LINKER_LIBS} proto ntdll)
else()
  target_link_libraries(caffe ${Caffe_LINKER_LIBS})
endif()

caffe_default_properties(caffe)

target_compile_definitions(caffe ${Caffe_DEFINITIONS})
if(Caffe_COMPILE_OPTIONS)
  target_compile_options(caffe ${Caffe_COMPILE_OPTIONS})
endif()
set_target_properties(caffe PROPERTIES
    VERSION   ${CAFFE_TARGET_VERSION}
    SOVERSION ${CAFFE_TARGET_SOVERSION}
    )

configure_file(${caffe_export_hdr_in} ${caffe_export_hdr})

# ---[ Tests
# add_subdirectory(test)

# ---[ Install
install(DIRECTORY ${Caffe_INCLUDE_DIR}/caffe DESTINATION include)
install(FILES ${proto_hdrs} DESTINATION include/caffe/proto)
install(TARGETS caffe proto EXPORT CaffeTargets DESTINATION lib)

file(WRITE ${PROJECT_BINARY_DIR}/__init__.py)
list(APPEND proto_python ${PROJECT_BINARY_DIR}/__init__.py)
install(PROGRAMS ${proto_python} DESTINATION python/caffe/proto)

