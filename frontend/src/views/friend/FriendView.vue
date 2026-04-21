<template>
  <div class="friend-view">
    <div class="friend-header">
      <h1 class="page-title">好友</h1>
      <p class="page-subtitle">与道友交流切磋</p>
    </div>

    <div class="friend-content">
      <SsCard title="我的好友" class="friend-list-card">
        <div class="friend-list">
          <div
            v-for="friend in friends"
            :key="friend.id"
            class="friend-item"
            @click="selectFriend(friend)"
          >
            <div class="friend-avatar">
              <span class="avatar-text">{{ friend.name[0] }}</span>
              <span v-if="friend.online" class="online-dot" />
            </div>
            <div class="friend-info">
              <h4 class="friend-name">{{ friend.name }}</h4>
              <span class="friend-realm">{{ friend.realm }}</span>
            </div>
            <div class="friend-actions">
              <SsButton type="ghost" size="small" @click.stop="sendMessage(friend.id)">
                私聊
              </SsButton>
              <SsButton type="primary" size="small" @click.stop="challengeFriend(friend.id)">
                切磋
              </SsButton>
            </div>
          </div>
          <div v-if="friends.length === 0" class="empty-state">
            暂无好友
          </div>
        </div>
      </SsCard>

      <SsCard title="添加好友" class="add-friend-card">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="输入道号搜索..."
          />
          <SsButton type="primary" @click="searchFriend">
            搜索
          </SsButton>
        </div>

        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="result in searchResults"
            :key="result.id"
            class="result-item"
          >
            <div class="result-avatar">
              <span>{{ result.name[0] }}</span>
            </div>
            <div class="result-info">
              <span class="result-name">{{ result.name }}</span>
              <span class="result-realm">{{ result.realm }}</span>
            </div>
            <SsButton type="gold" size="small" @click="addFriend(result.id)">
              添加
            </SsButton>
          </div>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'

interface Friend {
  id: string
  name: string
  realm: string
  online: boolean
}

const friends = ref<Friend[]>([
  { id: 'f1', name: '剑心', realm: '筑基期', online: true },
  { id: 'f2', name: '清风', realm: '练气期', online: false },
  { id: 'f3', name: '明月', realm: '金丹期', online: true },
])

const searchQuery = ref('')
const searchResults = ref<Friend[]>([])

function selectFriend(friend: Friend) {
  console.log('选择好友', friend)
}

function sendMessage(id: string) {
  console.log('发送消息', id)
}

function challengeFriend(id: string) {
  console.log('挑战好友', id)
}

function searchFriend() {
  if (!searchQuery.value) return
  searchResults.value = [
    { id: 's1', name: searchQuery.value, realm: '筑基期', online: true },
  ]
}

function addFriend(id: string) {
  console.log('添加好友', id)
  searchResults.value = searchResults.value.filter(f => f.id !== id)
}
</script>

<style scoped lang="scss">
.friend-view {
  max-width: 800px;
  margin: 0 auto;
}

.friend-header {
  text-align: center;
  margin-bottom: var(--space-6);
}

.page-title {
  font-family: var(--font-title);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: 0;
}

.friend-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.friend-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.friend-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
  }
}

.friend-avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.online-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  background: #27AE60;
  border-radius: 50%;
  border: 2px solid var(--bg-card);
}

.friend-info {
  flex: 1;
}

.friend-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-1);
}

.friend-realm {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.friend-actions {
  display: flex;
  gap: var(--space-2);
}

.empty-state {
  text-align: center;
  padding: var(--space-6);
  color: var(--text-muted);
}

.search-box {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.search-input {
  flex: 1;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  color: var(--text-primary);
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: var(--color-primary-light);
  }

  &::placeholder {
    color: var(--text-muted);
  }
}

.search-results {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.result-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.result-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: var(--text-primary);
}

.result-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-name {
  font-size: var(--text-sm);
  color: var(--text-primary);
}

.result-realm {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}
</style>
