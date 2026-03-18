import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Combine les classes Tailwind de maniere intelligente
 * @param  {...any} inputs - Classes CSS a combiner
 * @returns {string} Classes combinees
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

/**
 * Formate une date en francais
 * @param {Date|string} date - Date a formater
 * @param {object} options - Options de formatage
 * @returns {string} Date formatee
 */
export function formatDate(date, options = {}) {
  const defaultOptions = {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    ...options,
  }
  return new Intl.DateTimeFormat('fr-FR', defaultOptions).format(new Date(date))
}

/**
 * Formate une duree en heures et minutes
 * @param {number} minutes - Duree en minutes
 * @returns {string} Duree formatee
 */
export function formatDuration(minutes) {
  if (minutes < 60) {
    return `${minutes} min`
  }
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins > 0 ? `${hours}h ${mins}min` : `${hours}h`
}

/**
 * Tronque un texte avec ellipsis
 * @param {string} text - Texte a tronquer
 * @param {number} maxLength - Longueur maximale
 * @returns {string} Texte tronque
 */
export function truncate(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text
  return text.slice(0, maxLength).trim() + '...'
}

/**
 * Genere des initiales a partir d'un nom
 * @param {string} name - Nom complet
 * @returns {string} Initiales
 */
export function getInitials(name) {
  if (!name) return ''
  return name
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

/**
 * Formate un nombre avec separateur de milliers
 * @param {number} num - Nombre a formater
 * @returns {string} Nombre formate
 */
export function formatNumber(num) {
  return new Intl.NumberFormat('fr-FR').format(num)
}

/**
 * Formate un nombre de vues de maniere compacte
 * @param {number} views - Nombre de vues
 * @returns {string} Vues formatees
 */
export function formatViews(views) {
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`
  }
  if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`
  }
  return views.toString()
}

/**
 * Genere un slug a partir d'un texte
 * @param {string} text - Texte a transformer
 * @returns {string} Slug
 */
export function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)+/g, '')
}

/**
 * Delai d'attente
 * @param {number} ms - Millisecondes
 * @returns {Promise}
 */
export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Verifie si une URL est valide
 * @param {string} url - URL a verifier
 * @returns {boolean}
 */
export function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Obtient le niveau de difficulte en francais
 * @param {string} level - Niveau (BEGINNER, INTERMEDIATE, ADVANCED)
 * @returns {string} Niveau en francais
 */
export function getLevelLabel(level) {
  const levels = {
    BEGINNER: 'Debutant',
    INTERMEDIATE: 'Intermediaire',
    ADVANCED: 'Avance',
  }
  return levels[level] || level
}

/**
 * Obtient la couleur du badge selon le niveau
 * @param {string} level - Niveau
 * @returns {string} Classes Tailwind
 */
export function getLevelColor(level) {
  const colors = {
    BEGINNER: 'bg-green-100 text-green-700',
    INTERMEDIATE: 'bg-amber-100 text-amber-700',
    ADVANCED: 'bg-red-100 text-red-700',
  }
  return colors[level] || 'bg-gray-100 text-gray-700'
}
