import { useState } from 'react';
import { Heart, MessageCircle, Share2, MoreVertical } from 'lucide-react';
import { Card, CardContent, Avatar, Button } from '../components/ui';

export default function FeedPage() {
  const [posts] = useState([
    {
      id: 1,
      author: { name: 'Ahmed Hassan', avatar: '/placeholder.svg?height=40&width=40', role: 'Enseignant' },
      content: 'Nouvelle formation sur la jurisprudence islamique disponible maintenant!',
      image: '/placeholder.svg?height=300&width=500',
      likes: 245,
      comments: 32,
      shares: 18,
      timestamp: '2 heures ago',
      liked: false,
    },
    {
      id: 2,
      author: { name: 'Fatima Al-Rashid', avatar: '/placeholder.svg?height=40&width=40', role: 'Apprenant' },
      content: 'Juste terminé le cours sur le Tafsir. Vraiment enrichissant!',
      likes: 156,
      comments: 24,
      shares: 12,
      timestamp: '4 heures ago',
      liked: false,
    },
  ]);

  return (
    <div className="max-w-2xl mx-auto space-y-4 p-4">
      {/* Création de post */}
      <Card>
        <CardContent className="pt-4">
          <div className="flex gap-4">
            <Avatar size="md" src="/placeholder.svg?height=40&width=40" alt="Vous" />
            <div className="flex-1">
              <input
                type="text"
                placeholder="Partagez vos pensées..."
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <div className="mt-3 flex justify-end gap-2">
                <Button variant="outline" size="sm">Annuler</Button>
                <Button size="sm">Publier</Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Feed de posts */}
      {posts.map(post => (
        <Card key={post.id}>
          <CardContent className="pt-4">
            {/* Header du post */}
            <div className="flex justify-between items-start mb-4">
              <div className="flex gap-3">
                <Avatar src={post.author.avatar} alt={post.author.name} />
                <div>
                  <div className="font-semibold text-gray-900">{post.author.name}</div>
                  <div className="text-sm text-gray-500">{post.author.role} • {post.timestamp}</div>
                </div>
              </div>
              <button className="text-gray-500 hover:text-gray-700">
                <MoreVertical size={20} />
              </button>
            </div>

            {/* Contenu */}
            <p className="text-gray-800 mb-3">{post.content}</p>
            {post.image && (
              <img src={post.image} alt="Post" className="w-full rounded-lg mb-4" />
            )}

            {/* Actions */}
            <div className="flex justify-between border-t border-gray-200 pt-3 text-gray-600 text-sm">
              <button className="flex items-center gap-2 hover:text-primary transition-colors">
                <Heart size={18} />
                {post.likes}
              </button>
              <button className="flex items-center gap-2 hover:text-primary transition-colors">
                <MessageCircle size={18} />
                {post.comments}
              </button>
              <button className="flex items-center gap-2 hover:text-primary transition-colors">
                <Share2 size={18} />
                {post.shares}
              </button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
