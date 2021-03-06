/*
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#ifndef ONEFLOW_CORE_KERNEL_DECODE_RANDOM_KERNEL_H_
#define ONEFLOW_CORE_KERNEL_DECODE_RANDOM_KERNEL_H_

#include "oneflow/core/kernel/kernel.h"

namespace oneflow {

template<DeviceType device_type>
class DecodeRandomKernel final : public KernelIf<device_type> {
 public:
  OF_DISALLOW_COPY_AND_MOVE(DecodeRandomKernel);
  DecodeRandomKernel() = default;
  ~DecodeRandomKernel() = default;

  void Forward(const KernelCtx& ctx,
               std::function<Blob*(const std::string&)> BnInOp2Blob) const override {
    ForwardDataContent(ctx, BnInOp2Blob);
  }

  void ForwardDataContent(const KernelCtx& ctx,
                          std::function<Blob*(const std::string&)> BnInOp2Blob) const override;

 private:
  void VirtualKernelInit() override;
  uint32_t GenNextRandomSeed() const;

  std::unique_ptr<std::mt19937> gen_;
  std::unique_ptr<std::uniform_int_distribution<uint32_t>> dis_;

  mutable bool is_init_;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_KERNEL_DECODE_RANDOM_KERNEL_H_
