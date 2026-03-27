import { Heart, MessageCircle, Share2 } from 'lucide-react';
import { Card, CardContent } from '../components/ui';

export default function ReelsPage() {
  const reels = [
    {
      id: 1,
      title: 'Concept islamique du jour',
      creator: 'Dr. Ahmed',
      thumbnail: '/placeholder.svg?height=400&width=300',
      likes: 1200,
      comments: 345,
    },
    {
      id: 2,
      title: 'Histoire inspirante',
      creator: 'Fatima Al-Rashid',
      thumbnail: '/placeholder.svg?height=400&width=300',
      likes: 2100,
      comments: 567,
    },
  ];

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Reels</h1>

      <div className="grid gap-6">
        {reels.map(reel => (
          <Card key={reel.id}>
            <CardContent className="pt-4">
              <div className="relative overflow-hidden bg-gray-900 rounded-lg mb-4">
                <img
                  src={reel.thumbnail}
                  alt={reel.title}
                  className="w-full aspect-video object-cover hover:opacity-90 transition-opacity cursor-pointer"
                />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{reel.title}</h3>
              <p className="text-sm text-gray-600 mb-4">par {reel.creator}</p>
              
              <div className="flex justify-between text-gray-600 text-sm border-t border-gray-200 pt-3">
                <button className="flex items-center gap-2 hover:text-primary transition-colors">
                  <Heart size={18} />
                  {reel.likes}
                </button>
                <button className="flex items-center gap-2 hover:text-primary transition-colors">
                  <MessageCircle size={18} />
                  {reel.comments}
                </button>
                <button className="flex items-center gap-2 hover:text-primary transition-colors">
                  <Share2 size={18} />
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
