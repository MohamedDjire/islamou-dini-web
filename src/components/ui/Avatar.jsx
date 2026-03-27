export default function Avatar({ src, alt, size = 'md', className = '' }) {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };
  
  return (
    <img 
      src={src || '/placeholder.svg?height=40&width=40'} 
      alt={alt} 
      className={`${sizes[size]} rounded-full object-cover ${className}`}
    />
  );
}
