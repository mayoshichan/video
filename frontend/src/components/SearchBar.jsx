import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <Input
            type="text"
            placeholder="Search videos and channels..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-10 bg-zinc-800 border-zinc-700 text-white placeholder:text-gray-400 focus:border-zinc-600 transition-colors"
          />
        </div>
        <Button 
          type="submit" 
          className="bg-zinc-700 hover:bg-zinc-600 text-white transition-colors"
        >
          Search
        </Button>
      </div>
    </form>
  );
};

export default SearchBar;