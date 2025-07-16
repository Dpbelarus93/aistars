import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { 
  fetchChatSessions, 
  fetchMessages, 
  sendMessage, 
  setCurrentSession,
  addMessage 
} from '../store/slices/chatSlice';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { 
  Send, 
  MessageCircle, 
  Bot, 
  User, 
  Plus, 
  Paperclip 
} from 'lucide-react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

export const ChatPage: React.FC = () => {
  const dispatch = useDispatch();
  const { sessions, currentSession, messages, isLoading, error } = useSelector((state: RootState) => state.chat);
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [messageText, setMessageText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    dispatch(fetchChatSessions());
  }, [dispatch]);

  useEffect(() => {
    if (currentSession) {
      dispatch(fetchMessages(currentSession.id));
    }
  }, [dispatch, currentSession]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!messageText.trim() || !currentSession) return;

    const message = messageText.trim();
    setMessageText('');
    setIsTyping(true);

    try {
      await dispatch(sendMessage({ sessionId: currentSession.id, content: message }));
      
      // Симуляция ответа AI-ассистента
      setTimeout(() => {
        const aiResponse = {
          id: Date.now().toString(),
          sessionId: currentSession.id,
          senderId: 'ai-assistant',
          content: `Спасибо за ваше сообщение: "${message}". Я AI-ассистент консервс-сервиса. Чем могу помочь?`,
          type: 'TEXT' as const,
          isFromAI: true,
          sender: {
            id: 'ai-assistant',
            name: 'AI Ассистент',
            email: 'ai@conserv-service.com',
            role: 'ADMIN' as const,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          },
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        
        dispatch(addMessage(aiResponse));
        setIsTyping(false);
      }, 1000);
    } catch (error) {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSessionSelect = (session: any) => {
    dispatch(setCurrentSession(session));
  };

  const handleCreateNewSession = () => {
    // Создание новой сессии чата
    const newSession = {
      id: Date.now().toString(),
      participants: [user!],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    dispatch(setCurrentSession(newSession));
  };

  return (
    <div className="h-full flex bg-white rounded-lg shadow overflow-hidden">
      {/* Sessions Sidebar */}
      <div className="w-1/3 border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Чаты</h2>
            <button
              onClick={handleCreateNewSession}
              className="btn btn-primary p-2"
            >
              <Plus className="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto">
          {sessions.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <MessageCircle className="h-12 w-12 mx-auto mb-2 text-gray-400" />
              <p>Нет активных чатов</p>
              <button
                onClick={handleCreateNewSession}
                className="btn btn-primary mt-2 text-sm"
              >
                Начать новый чат
              </button>
            </div>
          ) : (
            <div className="space-y-1 p-2">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  onClick={() => handleSessionSelect(session)}
                  className={`p-3 rounded-lg cursor-pointer transition-colors ${
                    currentSession?.id === session.id
                      ? 'bg-blue-100 border-blue-200'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                      <Bot className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        AI Ассистент
                      </p>
                      {session.lastMessage && (
                        <p className="text-xs text-gray-500 truncate">
                          {session.lastMessage.content}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {currentSession ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                  <Bot className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    AI Ассистент
                  </h3>
                  <p className="text-sm text-gray-500">
                    Поддержка консервс-сервиса
                  </p>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {error && (
                <ErrorMessage message={error} className="mb-4" />
              )}
              
              {isLoading ? (
                <LoadingSpinner className="py-8" />
              ) : (
                <>
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.isFromAI ? 'justify-start' : 'justify-end'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.isFromAI
                            ? 'bg-gray-100 text-gray-900'
                            : 'bg-blue-600 text-white'
                        }`}
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          {message.isFromAI ? (
                            <Bot className="h-4 w-4" />
                          ) : (
                            <User className="h-4 w-4" />
                          )}
                          <span className="text-xs opacity-75">
                            {format(new Date(message.createdAt), 'HH:mm', { locale: ru })}
                          </span>
                        </div>
                        <p className="text-sm">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  
                  {isTyping && (
                    <div className="flex justify-start">
                      <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 text-gray-900">
                        <div className="flex items-center space-x-2">
                          <Bot className="h-4 w-4" />
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Message Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex items-center space-x-2">
                <button className="btn btn-secondary p-2">
                  <Paperclip className="h-4 w-4" />
                </button>
                <div className="flex-1 relative">
                  <textarea
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Введите сообщение..."
                    className="input w-full resize-none"
                    rows={1}
                    style={{ minHeight: '40px' }}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={!messageText.trim() || isTyping}
                  className="btn btn-primary p-2 disabled:opacity-50"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <MessageCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Выберите чат или создайте новый
              </h3>
              <p className="text-gray-500 mb-4">
                Начните разговор с AI-ассистентом для получения помощи
              </p>
              <button
                onClick={handleCreateNewSession}
                className="btn btn-primary"
              >
                Начать новый чат
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};