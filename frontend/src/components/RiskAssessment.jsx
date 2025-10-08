import React from 'react'
import { motion } from 'framer-motion'
import { Shield, AlertTriangle, CheckCircle, Info } from 'lucide-react'

const RiskAssessment = ({ analysisData }) => {
  const riskAssessment = analysisData?.risk_assessment

  if (!riskAssessment) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="card"
      >
        <div className="flex items-center space-x-3 mb-4">
          <Shield className="h-6 w-6 text-primary-400" />
          <h3 className="text-lg font-semibold text-slate-200">Risk Değerlendirmesi</h3>
        </div>
        <div className="text-center py-8">
          <Info className="h-12 w-12 text-slate-400 mx-auto mb-4" />
          <p className="text-slate-400">Risk değerlendirmesi mevcut değil</p>
        </div>
      </motion.div>
    )
  }

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'yüksek':
        return 'text-red-400 bg-red-900/20 border-red-500'
      case 'orta':
        return 'text-yellow-400 bg-yellow-900/20 border-yellow-500'
      case 'düşük':
        return 'text-green-400 bg-green-900/20 border-green-500'
      default:
        return 'text-slate-400 bg-slate-800 border-slate-600'
    }
  }

  const getRiskIcon = (level) => {
    switch (level?.toLowerCase()) {
      case 'yüksek':
        return <AlertTriangle className="h-5 w-5" />
      case 'orta':
        return <Info className="h-5 w-5" />
      case 'düşük':
        return <CheckCircle className="h-5 w-5" />
      default:
        return <Shield className="h-5 w-5" />
    }
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-red-400'
    if (score >= 40) return 'text-yellow-400'
    return 'text-green-400'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <div className="flex items-center space-x-3 mb-6">
        <Shield className="h-6 w-6 text-primary-400" />
        <h3 className="text-lg font-semibold text-slate-200">Risk Değerlendirmesi</h3>
      </div>

      {/* Risk Score */}
      <div className="text-center mb-6">
        <div className={`inline-flex items-center px-4 py-2 rounded-full border ${getRiskColor(riskAssessment.risk_level)}`}>
          {getRiskIcon(riskAssessment.risk_level)}
          <span className="ml-2 font-medium">{riskAssessment.risk_score}/100</span>
        </div>
        <p className={`text-lg font-bold mt-2 ${getScoreColor(riskAssessment.risk_score)}`}>
          {riskAssessment.risk_level?.toUpperCase()}
        </p>
        <p className="text-sm text-slate-400 mt-1">Gizlilik Skoru</p>
      </div>

      {/* Risk Factors */}
      {riskAssessment.risk_factors && riskAssessment.risk_factors.length > 0 && (
        <div className="mb-6">
          <h4 className="text-md font-medium text-slate-200 mb-3 flex items-center">
            <AlertTriangle className="h-4 w-4 text-red-400 mr-2" />
            Risk Faktörleri
          </h4>
          <ul className="space-y-2">
            {riskAssessment.risk_factors.map((factor, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-start space-x-2 text-sm"
              >
                <div className="w-2 h-2 bg-red-400 rounded-full mt-2 flex-shrink-0"></div>
                <span className="text-red-300">{factor}</span>
              </motion.li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {riskAssessment.recommendations && riskAssessment.recommendations.length > 0 && (
        <div>
          <h4 className="text-md font-medium text-slate-200 mb-3 flex items-center">
            <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
            Öneriler
          </h4>
          <ul className="space-y-2">
            {riskAssessment.recommendations.map((recommendation, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-start space-x-2 text-sm"
              >
                <div className="w-2 h-2 bg-green-400 rounded-full mt-2 flex-shrink-0"></div>
                <span className="text-green-300">{recommendation}</span>
              </motion.li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  )
}

export default RiskAssessment
