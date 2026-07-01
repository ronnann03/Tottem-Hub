interface WizardProgressProps {
  pasoActual: number
  totalPasos: number
  labels: string[]
}

export function WizardProgress({ pasoActual, totalPasos, labels }: WizardProgressProps) {
  return (
    <div className="w-full mb-8 px-4 md:px-12">
      <div className="flex items-center justify-between relative">
        {/* Background line connecting all steps */}
        <div className="absolute left-0 top-4 -translate-y-1/2 w-full h-[2px] bg-gray-200 z-0"></div>
        
        {/* Active progress line */}
        <div 
          className="absolute left-0 top-4 -translate-y-1/2 h-[2px] bg-[#0088b8] z-0 transition-all duration-300"
          style={{ width: `${((pasoActual - 1) / (totalPasos - 1)) * 100}%` }}
        ></div>

        {labels.map((label, i) => {
          const stepNumber = i + 1;
          const isCompleted = stepNumber < pasoActual;
          const isCurrent = stepNumber === pasoActual;
          
          return (
            <div key={i} className="relative z-10 flex flex-col items-center">
              <div className="bg-white p-1 rounded-full">
                <div 
                  className={`w-7 h-7 rounded-full flex items-center justify-center border-2 transition-all duration-300
                    ${isCompleted ? 'bg-[#0088b8] border-[#0088b8] text-white' : 
                      isCurrent ? 'border-[#0088b8] bg-white' : 'border-gray-300 bg-white'}`}
                >
                  {isCompleted ? (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
                  ) : isCurrent ? (
                    <div className="w-3 h-3 bg-[#0088b8] rounded-full"></div>
                  ) : (
                    null
                  )}
                </div>
              </div>
              
              <div className="mt-2 flex flex-col items-center">
                <span className={`text-[11px] font-medium ${isCurrent || isCompleted ? 'text-[#0088b8]' : 'text-gray-400'}`}>
                  Paso {stepNumber}
                </span>
                <span className={`text-xs mt-0.5 hidden md:block whitespace-nowrap ${isCurrent ? 'text-gray-900 font-semibold' : 'text-gray-500'}`}>
                  {label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  )
}