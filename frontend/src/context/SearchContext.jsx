import React, { createContext, useContext, useState } from 'react'

const SearchContext = createContext()

export const useSearch = () => {
  const context = useContext(SearchContext)
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider')
  }
  return context
}

export const SearchProvider = ({ children }) => {
  const [searchResults, setSearchResults] = useState(null)
  const [selectedProfile, setSelectedProfile] = useState(null)
  const [analysisData, setAnalysisData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const updateSearchResults = (results) => {
    setSearchResults(results)
    setError(null)
  }

  const selectProfile = (profile) => {
    setSelectedProfile(profile)
  }

  const updateAnalysisData = (data) => {
    setAnalysisData(data)
  }

  const setLoading = (loading) => {
    setIsLoading(loading)
  }

  const setErrorState = (error) => {
    setError(error)
    setIsLoading(false)
  }

  const resetSearch = () => {
    setSearchResults(null)
    setSelectedProfile(null)
    setAnalysisData(null)
    setError(null)
    setIsLoading(false)
  }

  const value = {
    searchResults,
    selectedProfile,
    analysisData,
    isLoading,
    error,
    updateSearchResults,
    selectProfile,
    updateAnalysisData,
    setLoading,
    setErrorState,
    resetSearch
  }

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  )
}
