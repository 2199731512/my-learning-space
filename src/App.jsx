import { useState } from 'react'

function App() {
  const [length, setLength] = useState('')
  const [width, setWidth] = useState('')
  const [height, setHeight] = useState('')

  // 判断输入是否全部有效（非空且为合法数字）
  const allValid =
    length !== '' && width !== '' && height !== '' &&
    !isNaN(Number(length)) && !isNaN(Number(width)) && !isNaN(Number(height))

  // 实时计算体积
  const volume = allValid
    ? (Number(length) * Number(width) * Number(height)).toFixed(2)
    : null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-md bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl p-6 sm:p-8">

        {/* 标题区域 */}
        <div className="text-center mb-8">
          <h1 className="text-xl sm:text-2xl font-bold text-white tracking-wide uppercase">
            混凝土体积计算器
          </h1>
          <p className="text-slate-400 text-sm mt-2">
            精确计算 · 工程必备
          </p>
        </div>

        {/* 输入区域 */}
        <div className="space-y-5">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2 uppercase tracking-wider">
              长度 / Length
            </label>
            <div className="relative">
              <input
                type="number"
                step="any"
                min="0"
                placeholder="0.00"
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className="w-full px-4 py-3 pr-12 text-base text-white border border-white/10 rounded-xl bg-white/5 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-150 placeholder:text-slate-600 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-medium pointer-events-none">
                m
              </span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2 uppercase tracking-wider">
              宽度 / Width
            </label>
            <div className="relative">
              <input
                type="number"
                step="any"
                min="0"
                placeholder="0.00"
                value={width}
                onChange={(e) => setWidth(e.target.value)}
                className="w-full px-4 py-3 pr-12 text-base text-white border border-white/10 rounded-xl bg-white/5 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-150 placeholder:text-slate-600 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-medium pointer-events-none">
                m
              </span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2 uppercase tracking-wider">
              高度 / Height
            </label>
            <div className="relative">
              <input
                type="number"
                step="any"
                min="0"
                placeholder="0.00"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
                className="w-full px-4 py-3 pr-12 text-base text-white border border-white/10 rounded-xl bg-white/5 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-150 placeholder:text-slate-600 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-medium pointer-events-none">
                m
              </span>
            </div>
          </div>
        </div>

        {/* 结果区域 */}
        <div className="mt-8 p-5 sm:p-6 rounded-xl border border-white/10 bg-white/5">
          {volume !== null ? (
            <div className="text-center">
              <p className="text-xs text-blue-400 uppercase tracking-wider font-medium mb-1">
                Volume Result
              </p>
              <p className="text-xs text-slate-500 mb-4">
                计算结果
              </p>
              <p className="text-4xl sm:text-5xl font-bold text-white tracking-tight">
                {volume}
                <span className="text-xl sm:text-2xl font-normal ml-2 text-blue-400">
                  m³
                </span>
              </p>
              <p className="text-xs text-slate-600 mt-4">
                L × W × H = V
              </p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-xs text-blue-400/50 uppercase tracking-wider font-medium mb-1">
                Volume Result
              </p>
              <p className="text-slate-600 text-sm mt-3">
                请输入完整的长、宽、高
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App
