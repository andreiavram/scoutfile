alter table photologue_gallery_photos add column sort_value int(11) null;

CREATE TABLE `photologue_gallery_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `gallery_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  UNIQUE KEY `gallery_id` (`gallery_id`,`site_id`),
  KEY `pg_to_dj_site` (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table photologue_photo change title_slug slug varchar(50) not null unique;

CREATE TABLE `photologue_photo_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `photo_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `photo_id` (`photo_id`,`site_id`),
  KEY `photologue_photo_site_site_id_1b6cdacfbf50f_fk_django_site_id` (`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;