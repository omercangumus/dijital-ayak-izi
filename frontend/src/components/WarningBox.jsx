import React from 'react'
import { motion } from 'framer-motion'
import { ShieldCheck, AlertTriangle } from 'lucide-react'

const WarningBox = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="card bg-slate-700 border-slate-600"
    >
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <ShieldCheck className="h-6 w-6 text-primary-400" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-slate-200 mb-2">
            Etik Kullanım Uyarısı
          </h3>
          <p className="text-slate-300 leading-relaxed">
            Bu araç, yalnızca kendi dijital ayak izinizi keşfetmeniz amacıyla tasarlanmıştır. 
            Tüm aramalar KVKK kapsamında, rızanızla ve sizin adınıza yapılır.
          </p>
          <div className="mt-4 p-3 bg-slate-800 rounded-lg border border-slate-600">
            <div className="flex items-center space-x-2 mb-2">
              <AlertTriangle className="h-4 w-4 text-yellow-400" />
              <span className="text-sm font-medium text-yellow-400">Yasal Uyarı</span>
            </div>
            <p className="text-xs text-slate-400">
              Bu araç KVKK ve diğer gizlilik yasalarına uygun olarak kullanılmalıdır. 
              Yasadışı kullanım yasaktır ve sorumluluk kullanıcıya aittir.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default WarningBox
