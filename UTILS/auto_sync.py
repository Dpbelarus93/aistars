#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import time
import logging

# Настройка логирования
logging.basicConfig(
    filename='auto_sync.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GitAutoSync:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.tracked_dirs = [
            'TELEGRAM_PARSER_MVP',
            'MEDIA_PROCESSING',
            'PROMPT_LIBRARY',
            'ISTARS_DOCS'
        ]
        
    def run_git_command(self, command):
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Git command failed: {e.stderr}")
            return None

    def check_changes(self):
        status = self.run_git_command(['git', 'status', '--porcelain'])
        if not status:
            return False
        
        # Проверяем изменения только в отслеживаемых директориях
        changed = False
        for line in status.split('\n'):
            if line:
                for dir in self.tracked_dirs:
                    if dir in line:
                        changed = True
                        break
        return changed

    def sync(self):
        if not self.check_changes():
            logging.info("No changes to sync")
            return

        # Добавляем изменения
        for dir in self.tracked_dirs:
            self.run_git_command(['git', 'add', dir])

        # Создаем коммит
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"🔄 Автоматическая синхронизация [{timestamp}]"
        self.run_git_command(['git', 'commit', '-m', commit_msg])

        # Отправляем изменения
        self.run_git_command(['git', 'pull', '--rebase', 'origin', 'main'])
        push_result = self.run_git_command(['git', 'push', 'origin', 'main'])
        
        if push_result is not None:
            logging.info(f"Successfully synced changes: {commit_msg}")
        else:
            logging.error("Failed to push changes")

def main():
    repo_path = '/Users/dpbelarus/Desktop/хочу еще'
    syncer = GitAutoSync(repo_path)
    
    while True:
        try:
            syncer.sync()
            # Проверяем каждые 5 минут
            time.sleep(300)
        except Exception as e:
            logging.error(f"Sync error: {str(e)}")
            time.sleep(60)  # При ошибке ждем минуту перед повторной попыткой

if __name__ == '__main__':
    main()
