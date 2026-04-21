<template>
  <div class="map-view">
    <div class="map-header">
      <h1 class="page-title">世界地图</h1>
      <p class="page-subtitle">探索蜀山世界的各个角落</p>
    </div>

    <div class="map-content">
      <SsCard title="地图" class="map-card">
        <div class="map-container">
          <div class="map-regions">
            <div
              v-for="region in regions"
              :key="region.name"
              :class="['region-item', { 'is-active': selectedRegion === region.name }]"
              @click="selectedRegion = region.name"
            >
              <h4 class="region-name">{{ region.name }}</h4>
              <div class="region-locations">
                <div
                  v-for="loc in region.locations"
                  :key="loc.id"
                  :class="['location-node', { 'is-current': loc.id === currentLocationId }]"
                  @click.stop="selectLocation(loc)"
                >
                  <div class="location-dot" :style="{ background: getDangerColor(loc.dangerLevel) }" />
                  <span class="location-name">{{ loc.name }}</span>
                  <span class="location-type">{{ loc.type }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </SsCard>

      <SsCard v-if="selectedLocation" title="地点详情" class="location-detail-card">
        <div class="detail-header">
          <h3 class="detail-name">{{ selectedLocation.name }}</h3>
          <div class="detail-tags">
            <span class="type-tag">{{ selectedLocation.type }}</span>
            <span class="danger-tag" :style="{ background: getDangerColor(selectedLocation.dangerLevel) }">
              危险度 {{ '★'.repeat(selectedLocation.dangerLevel) }}
            </span>
          </div>
        </div>

        <p class="detail-description">{{ selectedLocation.description }}</p>

        <div class="detail-resources">
          <h4>可获取资源</h4>
          <div class="resource-tags">
            <span v-for="resource in selectedLocation.resources" :key="resource" class="resource-tag">
              {{ resource }}
            </span>
          </div>
        </div>

        <div class="detail-connections">
          <h4>相邻地点</h4>
          <div class="connection-list">
            <span v-for="conn in selectedLocation.connections" :key="conn" class="connection-item">
              {{ conn }}
            </span>
          </div>
        </div>

        <div class="detail-actions">
          <SsButton type="primary" block @click="travelTo(selectedLocation.id)">
            前往此地
          </SsButton>
          <SsButton type="ghost" block @click="exploreLocation(selectedLocation.id)">
            探索
          </SsButton>
        </div>
      </SsCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import SsCard from '@/components/common/SsCard/SsCard.vue'
import SsButton from '@/components/common/SsButton/SsButton.vue'
import { useGameStore } from '@/stores/game'

const router = useRouter()
const gameStore = useGameStore()

const selectedRegion = ref('中原')
const selectedLocation = ref<MapLocation | null>(null)

interface MapLocation {
  id: string
  name: string
  type: string
  dangerLevel: number
  resources: string[]
  connections: string[]
  description: string
}

interface Region {
  name: string
  locations: MapLocation[]
}

const regions: Region[] = [
  {
    name: '中原',
    locations: [
      { id: 'emei', name: '峨眉山', type: '门派', dangerLevel: 1, resources: ['灵草', '矿石'], connections: ['青城山', '成都府'], description: '峨眉派所在地，山势雄伟，灵气充沛' },
      { id: 'qingcheng', name: '青城山', type: '门派', dangerLevel: 1, resources: ['灵草', '木材'], connections: ['峨眉山', '成都府'], description: '青城派所在地，幽静清雅，道法自然' },
      { id: 'chengdu', name: '成都府', type: '城市', dangerLevel: 0, resources: ['食物', '药材'], connections: ['峨眉山', '青城山', '长安城'], description: '西南重镇，繁华热闹，商贾云集' },
      { id: 'chang_an', name: '长安城', type: '城市', dangerLevel: 0, resources: ['食物', '装备'], connections: ['成都府', '华山'], description: '帝都所在，天下中心，龙脉汇聚' },
      { id: 'huashan', name: '华山', type: '野外', dangerLevel: 2, resources: ['矿石', '灵草'], connections: ['长安城'], description: '险峻奇绝，常有妖兽出没' },
    ],
  },
  {
    name: '北方',
    locations: [
      { id: 'binggong', name: '冰宫', type: '特殊', dangerLevel: 4, resources: ['冰晶', '寒铁'], connections: ['屠龙岛'], description: '极北之地，万年寒冰，神秘莫测' },
      { id: 'tulong', name: '屠龙岛', type: '副本', dangerLevel: 5, resources: ['龙鳞', '龙珠'], connections: ['冰宫'], description: '传说中的屠龙之地，凶险万分' },
    ],
  },
  {
    name: '南方',
    locations: [
      { id: 'miaojiang', name: '苗疆腹地', type: '野外', dangerLevel: 3, resources: ['毒草', '蛊虫'], connections: ['虫谷'], description: '苗疆深处，毒虫遍地，危机四伏' },
      { id: 'chonggu', name: '虫谷', type: '副本', dangerLevel: 4, resources: ['毒草', '灵虫'], connections: ['苗疆腹地'], description: '万虫之谷，凶险异常' },
    ],
  },
]

const currentLocationId = computed(() => 'emei')

function getDangerColor(level: number): string {
  const colors = ['#27AE60', '#F39C12', '#E67E22', '#E74C3C', '#C0392B']
  return colors[level] || '#95A5A6'
}

function selectLocation(loc: MapLocation) {
  selectedLocation.value = loc
}

function travelTo(locationId: string) {
  console.log('前往', locationId)
  gameStore.currentLocation = selectedLocation.value?.name || ''
}

function exploreLocation(locationId: string) {
  router.push('/explore')
}
</script>

<style scoped lang="scss">
.map-view {
  max-width: 900px;
  margin: 0 auto;
}

.map-header {
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

.map-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.map-container {
  min-height: 400px;
}

.map-regions {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.region-item {
  padding: var(--space-3);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--border-active);
  }

  &.is-active {
    border-color: var(--color-primary-light);
    background: rgba(45, 90, 123, 0.1);
  }
}

.region-name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.region-locations {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.location-node {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2);
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: var(--bg-hover);
  }

  &.is-current {
    border: 1px solid var(--color-primary-light);
    box-shadow: var(--shadow-primary);
  }
}

.location-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.location-name {
  font-size: var(--text-sm);
  color: var(--text-primary);
}

.location-type {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.detail-header {
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-default);
}

.detail-name {
  font-family: var(--font-title);
  font-size: var(--text-xl);
  color: var(--text-primary);
  margin: 0 0 var(--space-2);
}

.detail-tags {
  display: flex;
  gap: var(--space-2);
}

.type-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.danger-tag {
  font-size: var(--text-xs);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  color: var(--text-primary);
}

.detail-description {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--space-4);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.detail-resources,
.detail-connections {
  margin-bottom: var(--space-4);

  h4 {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    margin: 0 0 var(--space-2);
  }
}

.resource-tags,
.connection-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.resource-tag,
.connection-item {
  font-size: var(--text-xs);
  padding: 2px 8px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

@media (max-width: 768px) {
  .map-content {
    grid-template-columns: 1fr;
  }
}
</style>
